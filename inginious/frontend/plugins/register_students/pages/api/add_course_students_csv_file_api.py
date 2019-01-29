import os
import web

from inginious.frontend.plugins.utils.admin_api import AdminApi
from inginious.frontend.plugins.utils import get_mandatory_parameter

_static_folder_path = os.path.join(os.path.dirname(__file__), "static")


class AddCourseStudentsCsvFile(AdminApi):
    def API_POST(self):
        file = get_mandatory_parameter(web.input(), "file")
        course_id = get_mandatory_parameter(web.input(), "course")

        text = file.decode("utf-8")
        parsed_file = self._parse_csv_file(text)

        course = self.get_course_and_check_rights(course_id)

        target_row, target_col = self._search_column_on_csv_file("email", parsed_file)
        if not target_row and not target_col:
            return 200, {"status": "error", "text": "Please insert a csv file with a column named 'email'"}

        inserted_users = 0
        usernames = self._fetch_usernames_from_file(target_row + 1, target_col, parsed_file)
        for username in usernames:
            try:
                result = self.user_manager.course_register_user(course, username, '', True)
                if result:
                    inserted_users += 1
            except:
                pass

        return 200, {"status": "success", "text": "The process succeeded. Registered students: " + str(inserted_users)}

    @staticmethod
    def _fetch_usernames_from_file(target_row, target_col, csv_file):
        '''
        Thi method works when the usernames are present in the file as emails, so we need to fetch just the username
        associated to the email. (e.g. crdgonzalezca@unal.edu.co -> crdgonzalezca).
        :param target_row:
        :param target_col:
        :param csv_file:
        :return: A list containing the students' usernames.
        '''
        length_column = len(csv_file)
        return [csv_file[row][target_col].split("@")[0] for row in range(target_row, length_column) if
                csv_file[row][target_col]]

    @staticmethod
    def _search_column_on_csv_file(column_name, csv_file):
        '''
        Method that search for the location of cell with a specific name. This will be used to retrieve the students'
        usernames
        :param column_name: The name of the column you are searching for (e.g. "email").
        :param csv_file: The file as a matrix.
        :return: a pair with the location of the searched column. If the column is not present, returns None, None.
        '''
        target_row = -1
        target_col = -1
        for row in csv_file:
            target_row += 1
            target_col = -1
            for cell in row:
                target_col += 1
                if cell == column_name:
                    return target_row, target_col

        return None, None

    @staticmethod
    def _parse_csv_file(csv_file):
        '''
        Method that parses the csv file, splitting each row by a colon generating a matrix.
        :param csv_file: receives a list of strings (e.g. [",,,,", ",email, name,,"])
        :return: Matrix with the file parse. The return value looks like: [[,,,,], [,email, name,,]]
        '''
        csv_file = csv_file.split("\n")
        return [line.strip().split(",") for line in csv_file if line]
