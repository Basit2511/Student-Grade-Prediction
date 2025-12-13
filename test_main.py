import unittest
from unittest.mock import patch, mock_open
from io import StringIO
import numpy as np
from scipy import linalg

from main import Student, StudentManager

class TestStudent(unittest.TestCase):

  def test_student_creation(self):
    s = Student(student_id = "B018", name = "Basit", assignments = 90, exams = 78.5, attendance = 95, score = 86, grade = "A")
    self.assertEqual(s.student_id, "B018")
    self.assertEqual(s.name, "Basit")
    self.assertEqual(s.assignments, 90)
    self.assertEqual(s.exams, 78.5)
    self.assertEqual(s.attendance, 95)
    self.assertEqual(s.score, 86)
    self.assertEqual(s.grade, "A")

  def test_student_str(self):
    s = Student(student_id = "B018", name = "Basit", assignments = 90, exams = 78.5, attendance = 95, score = 86, grade = "A")
    st = str(s)
    self.assertIn("B018", st)
    self.assertIn("Basit", st)
    self.assertIn("A", st)

class TestStudentManager(unittest.TestCase):

  def setUp(self):
    self.sm = StudentManager()
  
  def test_valid_score_percent(self):
    self.assertEqual(self.sm.valid_score_percent(72), 72)
    self.assertEqual(self.sm.valid_score_percent(0), 0)
    self.assertEqual(self.sm.valid_score_percent(100), 100)
    self.assertEqual(self.sm.valid_score_percent(-5), -1)
    self.assertEqual(self.sm.valid_score_percent(105), -1)

  def test_valid_id(self):
    self.sm.add_student("0", "Basit", 90, 78.5, 95, 86, "A")
    self.assertEqual(self.sm.valid_id("1"), "1")
    self.assertEqual(self.sm.valid_id("0"), -1)

  def test_score_to_grade(self):
    self.assertEqual(self.sm.score_to_grade(95), "A")
    self.assertEqual(self.sm.score_to_grade(80.15), "B")
    self.assertEqual(self.sm.score_to_grade(79.55), "C")
    self.assertEqual(self.sm.score_to_grade(62), "D")
    self.assertEqual(self.sm.score_to_grade(59), "F")

  def test_add_student(self):
    self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
    self.assertEqual(len(self.sm.students), 1)
    self.assertEqual(self.sm.students[0].student_id, "B018")
    self.assertEqual(self.sm.students[0].name, "Basit")
    self.assertEqual(self.sm.students[0].assignments, 90)
    self.assertEqual(self.sm.students[0].exams, 78.5)
    self.assertEqual(self.sm.students[0].attendance, 95)
    self.assertEqual(self.sm.students[0].score, 86)
    self.assertEqual(self.sm.students[0].grade, "A")

  def test_view_students_no_student_data(self):
      with patch("sys.stdout", new=StringIO()) as fake_out:
          self.sm.view_students()
          output = fake_out.getvalue().strip()
          self.assertEqual(output, "No student data available.")

  def test_view_students_with_data(self):
      self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
      self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
      with patch("sys.stdout", new=StringIO()) as fake_out:
          self.sm.view_students()
          output = fake_out.getvalue().strip()
          self.assertIn("ID\tName\tAssignments\tExams\tAttendance\tGrade", output)
          self.assertIn("B018\tBasit\t90\t78.5\t95\tA", output)
          self.assertIn("F029\tAlice\t85\t88.0\t90\tA", output)

  def test_student_matrix_part_grade(self):
      self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
      self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
      self.sm.add_student("G057", "Bob", 70, 65.0, 80, 72, "C")
      with patch("sys.stdout", new=StringIO()) as fake_out:
          expected_matrix = np.array([[90, 78.5, 95],
                                     [85, 88.0, 90],
                                     [70, 65.0, 80]])
          np.testing.assert_array_equal(self.sm.student_matrix_part_grade(), expected_matrix)

  def test_student_matrix_grade(self):
      self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
      self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
      self.sm.add_student("G057", "Bob", 70, 65.0, 80, 72, "C")
      with patch("sys.stdout", new=StringIO()) as fake_out:
          expected_matrix = np.array([[86],
                                     [88],
                                     [72]])
          np.testing.assert_array_equal(self.sm.student_matrix_grade(), expected_matrix)

  def test_params_matrix_det_not_zero(self):
      self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
      self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
      self.sm.add_student("G057", "Bob", 70, 65.0, 80, 72, "C")
      A = self.sm.student_matrix_part_grade()
      g = self.sm.student_matrix_grade()
      params = self.sm.params_matrix_det_not_zero(A, g)
      self.assertEqual(params.shape, (3, 1))
      
  def test_params_matrix_det_zero(self):
      self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
      self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
      A = self.sm.student_matrix_part_grade()
      g = self.sm.student_matrix_grade()
      params = self.sm.params_matrix_det_zero(A, g)
      self.assertEqual(params.shape, (3, 1))

  def test_predict_factor_matrix_not_square(self):
    self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
    self.sm.add_student("G057", "Bob", 85, 88.0, 90, 88, "A")
    self.sm.add_student("Y078", "Charlie", 70, 65.0, 80, 72, "C")
    #self.assertEqual(self.sm.predict_factor(), -1)
  
  def test_predict_factor_det_zero(self):
    self.sm.add_student("B018", "Basit", 41, 42, 43, 43, "F")
    self.sm.add_student("F029", "Alice", 44, 45, 46, 45, "F")
    self.sm.add_student("G057", "Bob", 85, 87, 89, 87, "B")
    #self.assertEqual(self.sm.predict_factor(), 0)

  def test_predict_factor_det_not_zero(self):
    self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
    self.sm.add_student("G057", "Bob", 70, 65.0, 80, 72, "C")
    #self.assertEqual(self.sm.predict_factor(), 1)

  def test_predict_final_grade(self):
      self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
      self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
      self.sm.add_student("G057", "Bob", 70, 65.0, 80, 72, "C")
      params = self.sm.predict_factor()
      predicted_score = self.sm.predict_final_grade(80, 80, 90, params)
      self.assertTrue(isinstance(predicted_score, np.ndarray))
      self.assertEqual(predicted_score.shape, (1, 1))
      self.assertTrue(0 <= predicted_score[0][0] <=100)

  def test_update_students_no_data(self):
    with patch("sys.stdout", new=StringIO()) as fake_out:
      self.sm.update_student("NO007", "name")
      output = fake_out.getvalue().strip()
      self.assertEqual(output, "No student data saved yet.")

  def test_update_students_with_data_valid_item_name(self):
    self.sm.add_student(0, "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student(1, "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.update_student(1, "name")
    self.assertEqual(self.sm.students[1].name, 1)
    self.assertEqual(x, 1)

  def test_update_students_with_data_valid_item_assignments(self):
    self.sm.add_student(0, "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student(1, "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.update_student(0, "assignments")
    self.assertEqual(self.sm.students[0].assignments, 2)
    self.assertEqual(x, 1)

  def test_update_students_with_data_valid_item_exams(self):
    self.sm.add_student(0, "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student(1, "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.update_student(1, "exams")
    self.assertEqual(self.sm.students[1].exams, 3)
    self.assertEqual(x, 1)

  def test_update_students_with_data_valid_item_attendance(self):
    self.sm.add_student(0, "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student(1, "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.update_student(0, "attendance")
    self.assertEqual(self.sm.students[0].attendance, 4)
    self.assertEqual(x, 1)

  def test_update_students_with_data_valid_item_score(self):
    self.sm.add_student(0, "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student(1, "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.update_student(1, "score")
    self.assertEqual(self.sm.students[1].score, 5)
    self.assertEqual(x, 1)

  def test_update_students_with_data_invalid_item(self):
    self.sm.add_student(0, "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student(1, "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.update_student(1, "age")
    self.assertEqual(x, 0)
    with patch("sys.stdout", new=StringIO()) as fake_out:
      self.sm.update_student(1, "age")
      output = fake_out.getvalue().strip()
      expected_output = (
      "Invalid item. Please enter a valid item to edit."
    )
      self.assertEqual(output, expected_output)

  def test_update_students_with_data_invalid_id(self):
    self.sm.add_student(0, "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student(1, "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.update_student(9, "name")
    self.assertEqual(x, -1)
    with patch("sys.stdout", new=StringIO()) as fake_out:
      self.sm.update_student(9, "name")
      output = fake_out.getvalue().strip()
      expected_output = (
      "Invalid student id. Please enter a valid student id"
    )
      self.assertEqual(output, expected_output)

  def test_delete_student_no_data(self):
    with patch("sys.stdout", new=StringIO()) as fake_out:
      self.sm.delete_student(0)
      output = fake_out.getvalue().strip()
      self.assertEqual(output, "No contacts saved yet.")

  def test_delete_student_with_data_valid_id(self):
    self.sm.add_student(0, "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student(1, "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.delete_student(1)
    self.assertEqual(x, 1)

  def test_delete_student_with_data_invalid_id(self):
    self.sm.add_student(0, "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student(1, "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.delete_student(9)
    self.assertEqual(x, 0)
    with patch("sys.stdout", new=StringIO()) as fake_out:
      self.sm.delete_student(9)
      output = fake_out.getvalue().strip()
      expected_output = (
      "Invalid student id, please enter a valid student id"
    )
      self.assertEqual(output, expected_output)

  def test_delete_student_confirmation_yes(self):
    self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.delete_student_confirmation("F029", "Y")
    self.assertEqual(x, 1)  # Since we pop the student, no return value expected
    self.assertEqual(len(self.sm.students), 1)

  def test_delete_student_confirmation_no(self):
    self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
    x = self.sm.delete_student_confirmation("F029", "N")
    self.assertEqual(x, 0)
    self.assertEqual(len(self.sm.students), 2)

  def test_save_students_no_students(self):
    with patch("sys.stdout", new=StringIO()) as fake_out:
        self.sm.save_students()
        output = fake_out.getvalue().strip()
        self.assertEqual(output, "No student data saved yet.")
  
  def test_save_students_with_students(self):
    self.sm.add_student("B018", "Basit", 90, 78.5, 95, 86, "A")
    self.sm.add_student("F029", "Alice", 85, 88.0, 90, 88, "A")
    m = mock_open()
    with patch("builtins.open", m):
        self.sm.save_students()
         
    m().write.assert_any_call("B018\t--\tBasit\t--\t90\t--\t78.5\t--\t95\t--\t86\t--\tA\n")
    m().write.assert_any_call("F029\t--\tAlice\t--\t85\t--\t88.0\t--\t90\t--\t88\t--\tA\n")
    self.assertEqual(m().write.call_count, 2)

  def test_load_students(self):
    m = mock_open(read_data="B018\t--\tBasit\t--\t90\t--\t78.5\t--\t95\t--\t86\t--\tA\nF029\t--\tAlice\t--\t85\t--\t88.0\t--\t90\t--\t88\t--\tA\n")
    with patch("builtins.open", m):
        self.sm.load_students()
        self.assertEqual(len(self.sm.students), 2)
        self.assertEqual(self.sm.students[0].student_id, "B018")
        self.assertEqual(self.sm.students[0].name, "Basit")
        self.assertEqual(self.sm.students[1].exams, 88.0)
        self.assertEqual(self.sm.students[1].grade, "A")
        

if __name__ == '__main__':
  unittest.main()