/*
    Parses the class schedule table for the student's courses
*/

// Simple extractor for the times column to get Lecture, Lab, and Exam times. Returns empty string if there is no time
function getMeetingInfo(el) {
    var infoStr = "";
    el.find("div").each(function() {
        infoStr += $(this).text() + "/";
    });
    return infoStr;
}

// Return object
var enrollments = {
    "term": "W16",
    "courses": [],
};

// For each course name, and therefore each course row
$("a[id^='LIST_VAR6_']").each(function(i, e) {
    // Find the times column
    var timesCol = $($(e).closest("td")).siblings(".LIST_VAR12");

    enrollments["courses"].push({
        "name": $(e).text(), // Add course name
        "de": !!timesCol.find(".meet.Distance.Education").length, // Is it DE
        "lec": getMeetingInfo(timesCol.find(".LEC")),
        "lab": getMeetingInfo(timesCol.find(".LAB")),
        "exam": getMeetingInfo(timesCol.find(".EXAM")),
    });
});

// Selenium gets the return statement evaluation so this is weird but necessary
return enrollments;
