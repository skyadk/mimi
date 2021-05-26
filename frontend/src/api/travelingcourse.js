import { instance } from './index';

function postOptions(optionData) {
    return instance.post('recommendroad/recommend-travle', optionData);
}

export { postOptions, };