import { instance } from './index'

function postSearch(searchData) {
    return instance.post('recommendroad/main-storelist', searchData)
}

function postSearchKeyword(searchData) {
    return instance.post('recommendroad/keyword-storelist', searchData)
}

export { postSearch, postSearchKeyword, };