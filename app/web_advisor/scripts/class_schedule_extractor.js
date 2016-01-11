/*
    Parses the class schedule table for the student's courses
*/

// Simple extractor for the times column to get Lecture, Lab, and Exam times. Returns empty string if there is no time
function getMeetingInfo(el) {
    var meetingInfo = {};

    el.find("div").each(function(i) {
        if (i == 0) {
            meetingInfo["days"] = $(this).text().split(/[\s,]+/).slice(1);
        } else if (i == 1) {
            meetingInfo["time"] = $(this).text();
        } else if (i == 2) {
            meetingInfo["location"] = $(this).text();
        }
    });

    return meetingInfo;
}

// Return object
var enrollments = {
    "term": "W16",
    "courses": [],
};

// For each course name, and therefore each course row
$("a[id^='LIST_VAR6_']").each(function(i, e) {
    // Find the times column
    var timesCol = $($(e).closest("td")).siblings(".LIST_VAR12"),
        nameParts = $(e).text().split(/[*()]+/);

    enrollments["courses"].push({
        "name": nameParts[0] + "*" + nameParts[1] + " " + nameParts[nameParts.length - 1].trim(), // Add course name
        "de": !!timesCol.find(".meet.Distance.Education").length, // Is it DE
        "lec": getMeetingInfo(timesCol.find(".LEC")),
        "lab": getMeetingInfo(timesCol.find(".LAB")),
        "exam": getMeetingInfo(timesCol.find(".EXAM")),
    });
});

// Selenium gets the return statement evaluation so this is weird but necessary
return enrollments;
