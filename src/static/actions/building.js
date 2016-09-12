import fetch from 'isomorphic-fetch';
import { push } from 'react-router-redux';
import jwtDecode from 'jwt-decode';
import { SERVER_URL } from '../utils/config';
import { checkHttpStatus, parseJSON } from '../utils';
import {
    BUILDING_CREATE_REQUEST,
    BUILDING_CREATE_FAILURE,
    BUILDING_CREATE_SUCCESS,
    BUILDING_LIST_REQUEST,
    BUILDING_LIST_FAILURE,
    BUILDING_LIST_SUCCESS,
    BUILDING_GET_REQUEST,
    BUILDING_GET_FAILURE,
    BUILDING_GET_SUCCESS
} from '../constants';


export function buildingCreateSuccess(buildingID) {
    return {
        type: BUILDING_CREATE_SUCCESS,
        payload: {
            buildingID: buildingID 
        }
    };
}

export function buildingCreateFailure(error) {
    return {
        type: BUILDING_CREATE_FAILURE,
        payload: {
            status: error.response.status,
            statusText: error.response.statusText
        }
    };
}

export function buildingCreateRequest() {
    return {
        type: BUILDING_CREATE_REQUEST
    };
}

export function createBuilding(token, title, description, latitude, longitude, redirect) {
    return (dispatch) => {
        dispatch(buildingCreateRequest());
        return fetch(`${SERVER_URL}/api/v1/base/buildings`, {
            method: 'post',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                Authorization: `JWT ${token}`
            },
            body: JSON.stringify({
                title, description, 
                "latitude": parseFloat(latitude).toFixed(6),
                "longitude": parseFloat(longitude).toFixed(6),
            })
        })
            .then(checkHttpStatus)
            .then(parseJSON)
            .then(response => {
                try {
                    dispatch(buildingCreateSuccess(response));
                    dispatch(push(redirect));
                } catch (e) {
                    dispatch(buildingCreateFailure({
                        response: {
                            status: 403,
                            statusText: 'Error creating building.'
                        }
                    }));
                }
            })
            .catch(error => {
                dispatch(buildingCreateFailure(error));
            });
    };
}

export function buildingListSuccess(buildingList) {
    return {
        type: BUILDING_LIST_SUCCESS,
        payload: buildingList
    };
}

export function buildingListFailure(error) {
    return {
        type: BUILDING_LIST_FAILURE,
        payload: {
            status: error.response.status,
            statusText: error.response.statusText
        }
    };
}

export function buildingListRequest() {
    return {
        type: BUILDING_LIST_REQUEST
    };
}

export function listBuildings(token, rent=null, numBeds=null, numBaths=null) {
    let queryParams="";

    if (rent != null && numBeds != null && numBaths != null) {
        queryParams = "?rent=" + rent + "&num_beds=" + numBeds + "&num_baths=" + numBaths;
    }

    return (dispatch) => {
        dispatch(buildingListRequest());
        return fetch(`${SERVER_URL}/api/v1/base/buildings${queryParams}`, {
            method: 'get',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                Authorization: `JWT ${token}`
            },
        })
            .then(checkHttpStatus)
            .then(parseJSON)
            .then(response => {
                try {
                    dispatch(buildingListSuccess(response));
                } catch (e) {
                    dispatch(buildingListFailure({
                        response: {
                            status: 403,
                            statusText: e
                        }
                    }));
                }
            })
            .catch(error => {
                dispatch(buildingListFailure(error));
            });
    };
}

export function buildingGetSuccess(buildingGet) {
    return {
        type: BUILDING_GET_SUCCESS,
        payload: buildingGet
    };
}

export function buildingGetFailure(error) {
    return {
        type: BUILDING_GET_FAILURE,
        payload: {
            status: error.response.status,
            statusText: error.response.statusText
        }
    };
}

export function buildingGetRequest() {
    return {
        type: BUILDING_GET_REQUEST
    };
}

export function getBuilding(token, buildingID) {
    return (dispatch) => {
        dispatch(buildingGetRequest());
        return fetch(`${SERVER_URL}/api/v1/base/buildings/${buildingID}`, {
            method: 'get',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                Authorization: `JWT ${token}`
            },
        })
            .then(checkHttpStatus)
            .then(parseJSON)
            .then(response => {
                try {
                    dispatch(buildingGetSuccess(response));
                } catch (e) {
                    dispatch(buildingGetFailure({
                        response: {
                            status: 403,
                            statusText: e
                        }
                    }));
                }
            })
            .catch(error => {
                dispatch(buildingGetFailure(error));
            });
    };
}
