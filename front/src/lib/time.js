//change gmt time to local time
export default function gmtToLocal(gmtTime) {
  var time = String(gmtTime).split("T");
  var changedTime = new Date(time[0] + " " + time[1] + " GMT").toLocaleString();
  return changedTime;
}
