import { instance } from './index';

function getStoreReview(sid) {
    return instance.get(`recommendroad/get-all-review/${sid}`);
}

function getStoreInfo(sid) {
    return instance.get(`recommendroad/get-store-info/${sid}`);
}

function getStoreLocation(sid) {
    return instance.get(`recommendroad/get-store-locate/${sid}`);
}

export { getStoreReview, getStoreInfo, getStoreLocation, };