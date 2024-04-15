import csv
from dataclasses import dataclass
import operator

@dataclass(order=True)
class Course:
    class_name: str
    course_code: str
    course_name_in_English: str
    credits: int
    link_to_syllabus: str
    materials: str
    number_of_students: int
    objective: str
    upper_limit: int
    year: int
        
def get_courses():
    course_list = []
    # Open csv file
    with open('semCourseSpider/course_data.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        is_first_row = True
        for row in reader:
            if is_first_row:
                is_first_row = False
                continue
            course_list.append(Course(
                class_name=row[0],
                course_code=row[1],
                course_name_in_English=row[2],
                credits=row[3],
                link_to_syllabus=row[4],
                materials=row[5],
                number_of_students=row[6],
                objective=row[7],
                upper_limit=row[8],
                year=row[9],
            ))
    return sorted(course_list, key=operator.attrgetter("year"))

def main():
    year = None
    # Open HTML file
    with open("course.html", "w") as webpage_file:
        # Write HTML file
        webpage_file.write('''<html>
        <head>
            <title>List of course</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        </head>
        <body>
            <h1 class='text-center m-3'>Computer Science and Information Engineering Bachelor Course</h1>
                        ''')
        # loop per course
        for course in get_courses():
            if year is None:
                # Assign from the smallest number
                year = course.year
                webpage_file.write("<div class='container'>")
                webpage_file.write(f"<h2 class='my-3' id=year{year}>Year {year}</h2>")
                webpage_file.write(f'''<div class="container">
                                        <div class="row g-3 gx-3">''')
            if year != course.year:
                # If the year change, 
                year = course.year
                # Close the section
                webpage_file.write('''</div>
                                    </div>''')
                webpage_file.write("</div>")
                webpage_file.write("<div class='container'>")
                # Add h2
                webpage_file.write(f"<h2 class='my-3' id=year{year}>Year {year}</h2>")
                webpage_file.write(f'''<div class="container">
                                        <div class="row g-3 gx-3">''')
            # Make the course cards
            webpage_file.write(f'''
                            <div class="card w-50" style="width: 18rem;">
                                <div class="card-body">
                                    <h5 class="card-title">{course.course_name_in_English}</h5>
                                    <div class="container text-center">
                                        <div class="row">
                                            <div class="col">
                                                <span class="fw-bold">Course code:</span> {course.course_code}
                                            </div>
                                            <div class="col">
                                                <span class="fw-bold">Credits:</span> {course.credits}
                                            </div>
                                            <div class="col">
                                                <span class="fw-bold">Number of students:</span> {course.number_of_students}/{course.upper_limit}
                                            </div>
                                        </div>
                                    </div>
                                    <p class="card-text">{course.objective}</p>
                                    <a href="{course.link_to_syllabus}" class="btn btn-primary">Details</a>
                                </div>
                            </div>
                            ''')
        webpage_file.write('''
        </body>
    </html>''')

main()