//change gmt time to local time
export default function gmtToLocal(dateTime) { return (new Date(Date.parse(dateTime) + 9 * 60 * 60 * 1000)).toLocaleString() };
