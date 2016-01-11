function getMeetingInfo(el) {
    var infoStr = "";
    el.find("div").each(function() {
        infoStr += $(this).text() + "/";
    });
    return infoStr;
}

var enrollments = {
    "term": "W16",
    "courses": [],
};

$("a[id^='LIST_VAR6_']").each(function(i, e) {
    var timesCol = $($(e).closest("td")).siblings(".LIST_VAR12");

    enrollments["courses"].push({
        "name": $(e).text(),
        "de": !!timesCol.find(".meet.Distance.Education").length,
        "lec": getMeetingInfo(timesCol.find(".LEC")),
        "lab": getMeetingInfo(timesCol.find(".LAB")),
        "exam": getMeetingInfo(timesCol.find(".EXAM")),
    });
});

return enrollments;
