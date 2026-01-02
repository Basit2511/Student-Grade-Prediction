import numpy as np
from scipy import linalg

class Student:

  def __init__(self, student_id, name, assignments, exams, attendance, score, grade):
    self.student_id = student_id
    self.name = name
    self.assignments = assignments
    self.exams = exams
    self.attendance = attendance
    self.grade = grade
    self.score = score

  def __str__(self):
    return f"{self.student_id:10} {self.name:10} {self.assignments:10} {self.exams:7} {self.attendance:12} {self.score:10} {self.grade:10}"

class StudentManager: 
   
  def __init__(self):
    self.students = []

  def valid_score_float(self, prompt):
    while True:
      score = input(prompt)
      try:
        score = float(score)
        break
      except ValueError:
        print("Invalid score. Please enter a valid score.\n")
    return score
  
  def valid_score_percent(self, score):
    while True:
      if float(score) < 0 or float(score) > 100:
        print(
            "Invalid input. Please enter a real percentage\n"
        )
        return -1
      else:
        return float(score)

  def valid_id(self, student_id):
    student_id = str(student_id)
    for s in self.students:
      if student_id in s.student_id:
        print("\nID has already been used. Please enter another ID\n")
        return -1
      else:
        continue
    return student_id 
      
  def score_to_grade(self, score):
    if score >= 90:
      return "A"
    elif score >= 80:
      return "B"
    elif score >= 70:
      return "C"
    elif score >= 60:
      return "D"
    else:
      return "F"

  def add_student(self, student_id, name, assignments, exams, attendance, score, grade):
    s = Student(student_id, name, assignments, exams, attendance, score, grade)
    self.students.append(s)
    return 1

  def view_students(self):
    if not self.students:
      print("\nNo student data available.\n\n")
    else:
      print("\nID\tName\tAssignments\tExams\tAttendance\tGrade\n")
      for s in self.students:
        print(
          f"{s.student_id}\t{s.name}\t{s.assignments}\t\t{s.exams}\t{s.attendance}\t\t{s.grade}\n"
        )

  def student_matrix_part_grade(self):
    A_vector = []
    for s in self.students:
      A_vector.append([s.assignments, s.exams, s.attendance])
    A = np.array(A_vector)
    return A

  def student_matrix_grade(self):
    g_vector = []
    for s in self.students:
      g_vector.append([s.score])
    g = np.array(g_vector)
    return g

  def params_matrix_det_not_zero(self, A, g):
    A_inv = linalg.inv(A)
    params = A_inv @ g
    return params

  def params_matrix_det_zero(self, A, g):
    A_pinv = linalg.pinv(A)
    params = A_pinv @ g
    return params

  def predict_factor(self):
    A = self.student_matrix_part_grade()
    g = self.student_matrix_grade()
    if len(self.students) != 3:
      params = self.params_matrix_det_zero(A, g)
      return params
      #z = -1
      #return z # z=-1 if len(students)!=3 and used for testing purposes
    det_A = linalg.det(A)
    if det_A == 0:
      params = self.params_matrix_det_zero(A, g)
      return params 
      #z = 0
    else:
      params = self.params_matrix_det_not_zero(A, g)
      return params 
      #z = 1
    #return z # z=1 if det(A) !=0 else 0 and used for testing purposes
    
  def predict_final_grade(self, predict_assignment, predict_exam, predict_attendance, params):
    student_result = np.array([[predict_assignment, predict_exam, predict_attendance]])
    predicted_score = student_result @ params
    return predicted_score

  def update_student(self, id, item):
    if not self.students:
      print("\nNo student data saved yet.\n\n")
    else:
      z = 0
      for s in self.students:
        if id == s.student_id:
          z = 1
          if item == "name":
            s.name = input("\nEnter new name:\n> ")  #commented out during testing
            #s.name = 1 #-- used during testing
            return 1
          elif item == "assignments":
            prompt = "\nEnter new assignment score (%):\n> "
            assignments_float = self.valid_score_float(prompt) #commented out during testing
            s.assignments = self.valid_score_percent(assignments_float) #commented out during testing
            #s.assignments = 2 #-- used during testing
            return 1
          elif item == "exams":
            prompt = "\nEnter new exam score (%):\n> "
            exams_float = self.valid_score_float(prompt) #commented out during testing
            s.exams = self.valid_score_percent(exams_float) #commented out during testing
            #s.exams = 3 #-- used during testing
            return 1
          elif item == "attendance":
            prompt = "\nEnter new attendance score (%):\n> "
            attendance_float = self.valid_score_float(prompt) #commented out during testing
            s.attendance = self.valid_score_percent(attendance_float) #commented out during testing
            #s.attendance = 4 #-- used during testing
            return 1
          elif item == "score":
            prompt = "\nEnter new final score (%):\n> "
            score_float = self.valid_score_float(prompt) #commented out during testing
            s.score = self.valid_score_percent(score_float) #commented out during testing
            s.grade = self.score_to_grade(s.score)
            #s.score = 5 #-- used during testing
            return 1
          else:
            print("\nInvalid item. Please enter a valid item to edit.\n\n")
            return 0
        else:
          continue
      if z != 1:
        print(
            "\nInvalid student id. Please enter a valid student id\n\n"
        )
        return -1
  
  def delete_student(self, student_id):
    z = 0
    if not self.students:
      print("\nNo contacts saved yet.\n\n")
    else:
      for s in self.students:
        if s.student_id == student_id:
          z = 1
        else:
          continue
      if z != 1:
        print("\nInvalid student id, please enter a valid student id\n")
      return z
    
  def delete_student_confirmation(self, student_id, confirmation):
    if confirmation == "Y":
      for idx,s in enumerate(self.students):
        if student_id in s.student_id:
          self.students.pop(idx)
          break
      return 1
    elif confirmation == "N":
      return 0
    else:
      print("Invalid input. Please enter Y or N.\n")
      return -1
    
  def save_students(self):
    if not self.students:
      print("\nNo student data saved yet.\n\n")
    else:
      with open("Downloads\grade_prediction\student_data.txt", "a") as f:
        for s in self.students:
          f.write(
            f"{s.student_id}\t--\t{s.name}\t--\t{s.assignments}\t--\t{s.exams}\t--\t{s.attendance}\t--\t{s.score}\t--\t{s.grade}\n"
        )
    return 1

  def load_students(self):
    with open("Downloads\grade_prediction\student_data.txt", "r") as f:
      for line in f:
        student_id, name, assignments, exams, attendance, score, grade = line.strip().split("\t--\t")
        s = Student(student_id, name, float(assignments), float(exams), float(attendance), float(score), grade)
        self.students.append(s)


def int_verif(prompt):
  while True:
    option = input(prompt)
    try:
      option = int(option)
      break
    except ValueError:
      print("\nInvalid input. Please enter a valid integer\n")
  return int(option)

def range_verification(option):
  while True:
    try:
      if int(option) < 1 or int(option) > 6:
        print(
            "Invalid input. Please enter a number within the signified range\n"
        )
        option = input("Enter an option(1-6): ")
      else:
        break
    except ValueError:
      print(
          "Invalid input. Please enter a number within the signified range\n")
      option = input("Enter an option(1-6): ")
  return int(option)

def result_verification(prompt):
  while True:
    result_is_float = students.valid_score_float(prompt)
    result = students.valid_score_percent(result_is_float)
    if result != -1:
      return result


if __name__ == "__main__":
  
  students = StudentManager()

  print("-----------------------------------------")
  print("\tSTUDENT GRADES PREDICTOR")
  print("-----------------------------------------\n")
  print("1. Add New Student data")
  print("2. View All Student data")
  print("3. Predict Final Grade for a Student")
  print("4. Update existing Student data")
  print("5. Delete Student data")
  print("6. Save and Exit\n")
  print("Note: All inputs entered that are not numbers are case-sensitive\n")

  students.load_students()

  while True:
    option = int_verif("Enter an option(1-6): ")
    x = range_verification(option)

    match x:
      case 1:
        print("\n")
        while True:
          student_id_prompt = input("Enter ID: ")
          student_id = students.valid_id(student_id_prompt)
          if student_id != -1:
            break
        name = input("Enter name: ")
        assignments = result_verification("Enter assignment score: ")
        exams = result_verification("Enter exam score: ")
        attendance = result_verification("Enter attendance score: ")
        score = result_verification("Enter final score: ")
        grade = students.score_to_grade(score)
        students.add_student(student_id, name, assignments, exams, attendance, score, grade)
        print("\nStudent data added successfully!")
        print("\n")
      case 2:
        students.view_students()
      case 3:
        factor = students.predict_factor()
        print("\n")
        assignments = result_verification("Enter assignment score: ")
        exams = result_verification("Enter exam score: ")
        attendance = result_verification("Enter attendance score: ")
        predicted_score = students.predict_final_grade(assignments, exams, attendance, factor)
        predicted_grade = students.score_to_grade(predicted_score)
        print(f"\nPredicted Final Score: {predicted_score[0][0]:.2f}%")
        print(f"Predicted Final Grade: {predicted_grade}")
        print("\n")
      case 4:
        students.view_students()
        id = input("Enter the ID of the student you want to update:\n> ")
        item = input("Enter the item you want to update (name, assignments, exams, attendance, score):\n> ")
        while True:
          updated_item = students.update_student(id, item)
          if updated_item == 1:
            print("\nStudent data updated successfully!\n")
            break
          else:
            id = input("Enter the ID of the student you want to update:\n> ")
            item = input("Enter the item you want to update (name, assignments, exams, attendance, score):\n> ")
        print("\n")
      case 5:
        students.view_students()
        z = 0
        student_id = input("Enter the ID of the student you want to delete:\n> ")
        while True:
          z = students.delete_student(student_id)
          if z == 1:
            confirmation = input("Are you sure you want to delete this student? (Y/N):\n> ")
            while True:
              deletion_status = students.delete_student_confirmation(student_id, confirmation)
              if deletion_status == 1:
                print("\nStudent data deleted successfully!\n")
                break
              elif deletion_status == 0:
                print("\nStudent data not deleted.\n")
                break
              else:
                confirmation = input("Are you sure you want to delete this student? (Y/N):\n> ")
            break
          else:
            student_id = input("Enter the ID of the student you want to delete:\n> ")
        print("\n")
      case 6:
        students.save_students()
        print("\nStudent data saved successfully! Exiting program...\n")
        break
      case _:
        print("should never see this")
