import os
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from base.models import Building, Unit, Review, Favorite
from accounts.models import User
from base.serializers import BuildingSerializer,\
        UnitSerializer, ReviewSerializer,\
        FullBuildingSerializer, UserSerializer, FavoriteSerializer,\
        ShareFavoriteSerializer, PasswordRecoverySerializer,\
        PasswordResetSerializer
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import ObjectDoesNotExist
import uuid


class IndexView(View):
    def get(self, request):
        abspath = open(os.path.join(
            settings.BASE_DIR, 'static_dist/index.html'), 'r')
        return HttpResponse(content=abspath.read())


class BuildingViewset(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    serializer_class = BuildingSerializer

    # This is for retrieving a building - used for favorites
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FullBuildingSerializer
        return BuildingSerializer

    def get_queryset(self):
        try:
            rent = self.request.query_params.get('rent')
            num_beds = self.request.query_params.get('num_beds')
            num_baths = self.request.query_params.get('num_baths')
            building_ids = Unit.objects.all().\
                filter(rent__lte=rent, num_beds__gte=num_beds,
                       num_baths__gte=num_baths).\
                values_list('building', flat=True)
            queryset = Building.objects.all().filter(pk__in=building_ids)
            return queryset

        # If no  or bad params, return everything
        except ValueError:
            return Building.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class UnitViewset(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    # This is for retrieving a unit - used for favorites
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # Get my own
    def list(self, request):
        queryset = Unit.objects.filter(creator=self.request.user).\
            order_by('date_created')
        serializer = UnitSerializer(queryset, many=True,
                                    context={'request': request})
        return Response({"results": serializer.data})


class ReviewViewset(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class FavoriteViewset(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    queryset = Favorite.objects.all().order_by('date_created')
    serializer_class = FavoriteSerializer

    @list_route(methods=['post'])
    def share(self, request):
        sf = ShareFavoriteSerializer(data=request.data)
        if sf.is_valid():
            email_text = "Hey,<br/><br/>" + request.user.first_name +\
                " has shared their favorite listings on " +\
                "<a href='" + settings.DOMAIN + "'/>GNDAPTS</a> " +\
                "with you. Check them out:" +\
                "<br/><br/>"

            destination = ""
            for e in sf.validated_data['emails']:
                destination += e + ","
            destination = destination[:-1]

            for f in request.user.favorite_set.filter(active=1):
                url = title = ""
                if f.unit is not None:
                    url = settings.DOMAIN + "/unit/show/" + str(f.unit.pk)
                    title = f.unit.title
                else:
                    url = settings.DOMAIN + "/building/show/" +\
                            str(f.building.pk)
                    title = f.building.title

                email_text += "<a href='" + url + "'/>" + title + "</a><br/>"

            email_text += "<br/>-GNDAPTS team"

            url = "https://api.mailgun.net/v3/" +\
                settings.MAILGUN_DOMAIN + "/messages"

            files = {
                'from': 'gndapts@mail.gndapts.com',
                'to': destination,
                'cc': request.user.email,
                'subject': request.user.first_name + " has shared their " +
                        "favorite listings from GNDAPTS with you",
                'html': email_text
                }

            requests.post(url, auth=('api', settings.MAILGUN_API_KEY),
                          data=files)

            # Deactivate favorites
            request.user.favorite_set.filter(active=1).update(active=0)

            return Response({}, status=status.HTTP_200_OK)

        return Response(sf.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class UserViewSet(
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        if request.user and pk == 'current':
            return Response(UserSerializer(request.user).data)
        return super(UserViewSet, self).retrieve(request, pk)

    @list_route(methods=['get'])
    def favoritescount(self, request):
        data = {"active_favorite_count":
                request.user.favorite_set.filter(active=1).count()}
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['post'], permission_classes=[])
    def sendpasswordrecoveryinstructions(self, request):
        pri = PasswordRecoverySerializer(data=request.data)
        if pri.is_valid():
            try:
                u = User.objects.get(email=pri.validated_data['email'])
                code = uuid.uuid4()
                u.recovery_key = code
                u.save()

                email_text = "Click here to reset your password:" +\
                    "<br/><br/>" +\
                    "<a href='" + settings.DOMAIN + "/resetpassword?code=" +\
                    str(code) + "'/>" +\
                    "Reset password</a>"

                email_text += "<br/><br/>-GNDAPTS team"

                url = "https://api.mailgun.net/v3/" +\
                    settings.MAILGUN_DOMAIN + "/messages"

                files = {
                    'from': 'gndapts@mail.gndapts.com',
                    'to': u.email,
                    'subject': "Recover password on GNDAPTS",
                    'html': email_text
                }

                requests.post(url, auth=('api', settings.MAILGUN_API_KEY),
                              data=files)

            # Can't reveal whether this worked or not for
            # security reasons
            except ObjectDoesNotExist:
                pass

            return Response({}, status=status.HTTP_200_OK)

        return Response(pri.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'], permission_classes=[])
    def resetpassword(self, request):
        pr = PasswordResetSerializer(data=request.data)
        if pr.is_valid():
            try:
                u = User.objects.get(recovery_key=pr.validated_data['code'])
                u.set_password(pr.validated_data['password'])
                u.recovery_key = None
                u.save()

            except ObjectDoesNotExist:
                return Response({"code": "Invalid or expired reset link."},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({}, status=status.HTTP_200_OK)

        return Response(pr.errors, status=status.HTTP_400_BAD_REQUEST)
