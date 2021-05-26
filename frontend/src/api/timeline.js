import { instance } from './index';

function getSchedule(num) {
    return instance.get(`recommendroad/get-user-schedule/${num}`)
}

export { getSchedule, };