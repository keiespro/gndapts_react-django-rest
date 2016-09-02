import React from 'react';
import { Route, IndexRoute } from 'react-router';
import App from './app';
import { HomeView, LoginView, ProtectedView, NotFoundView, SignupView,
    ConfirmEmailView, LoggedInView, MapView, AddBuildingView, PaddedContainer, AddUnitView, AddReviewView} from './containers';
import { requireAuthentication } from './utils/requireAuthentication';

export default(
    <Route path="/" component={App}>
        <IndexRoute component={LoginView}/>
        <Route path="signup" component={SignupView}/>
        <Route path="confirm/email/:code" component={ConfirmEmailView}/>
        <Route component={LoggedInView}>
            <Route path="home" component={requireAuthentication(HomeView)}/>
            <Route path="map" component={requireAuthentication(MapView)}/>
            <Route component={PaddedContainer}>
                <Route path="building/add" component={requireAuthentication(AddBuildingView)}/>
                <Route path="unit/add" component={requireAuthentication(AddUnitView)}/>
                <Route path="review/add" component={requireAuthentication(AddReviewView)}/>
            </Route>
        </Route>
        <Route path="protected" component={requireAuthentication(ProtectedView)}/>
        <Route path="*" component={NotFoundView}/>
    </Route>
);
