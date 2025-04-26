import threading
import time
import sys
from collections import deque

# Global lock for synchronization
lock = threading.Lock()

## Scene 1: Exam Hall Implementation
class ExamHallScene:
    def __init__(self):
        self.s0 = [0, 0, 0]  # Student 0 resources (pen, paper, question paper)
        self.s1 = [0, 0, 0]  # Student 1 resources
        self.s2 = [0, 0, 0]  # Student 2 resources

    def exit_scene(self):
        print("\n\n\n\t Thank You. \nSubmitted To: \nMs. Anamika Arora. \n\n\nSubmitted By: \nSamarth Agarwal (Team Leader) G-1 \nKunwardeep Singh H-2 \nLakshaydeep Chaudhary K-2\n")
        time.sleep(2)
        sys.exit(0)

    def assign(self, x, y):
        """Prevents students from having same resources."""
        if y == 0:  # Student 0
            if self.s1[x] == 1 or self.s2[x] == 1:
                print("\nTwo students can't have same resources.")
                self.exit_scene()
        elif y == 1:  # Student 1
            if self.s0[x] == 1 or self.s2[x] == 1:
                print("\nTwo students can't have same resources.")
                self.exit_scene()
        elif y == 2:  # Student 2
            if self.s0[x] == 1 or self.s1[x] == 1:
                print("\nTwo students can't have same resource.")
                self.exit_scene()
        return 1

    def student0(self):
        print("\nPress 1 for Pen, 2 for Paper and 3 for Question Paper")
        print("Enter the item present with 1st student: ", end="")
        try:
            a = int(input())
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        with lock:
            if a == 1:
                self.s0[0] = self.assign(0, 0)
            elif a == 2:
                self.s0[1] = self.assign(1, 0)
            elif a == 3:
                self.s0[2] = self.assign(2, 0)
            else:
                print("A student isn't configured to contain this.")

    def student1(self):
        print("Enter the item present with 2nd student: ", end="")
        try:
            a = int(input())
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        with lock:
            if a == 1:
                self.s1[0] = self.assign(0, 1)
            elif a == 2:
                self.s1[1] = self.assign(1, 1)
            elif a == 3:
                self.s1[2] = self.assign(2, 1)
            else:
                print("A student isn't configured to contain this.")

    def student2(self):
        print("Enter the item present with 3rd student: ", end="")
        try:
            a = int(input())
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        with lock:
            if a == 1:
                self.s2[0] = self.assign(0, 2)
            elif a == 2:
                self.s2[1] = self.assign(1, 2)
            elif a == 3:
                self.s2[2] = self.assign(2, 2)
            else:
                print("A student isn't configured to contain this.")

    def checking(self, a, b):
        if (a == 1 and b == 2) or (a == 2 and b == 1):
            return 3
        elif (a == 1 and b == 3) or (a == 3 and b == 1):
            return 2
        elif (a == 2 and b == 3) or (a == 3 and b == 2):
            return 1
        else:
            print("\nPlease check your input; Your input might be wrong or You have entered the same resources twice which will yield no result.\n")
            self.exit_scene()
            return 0

    def checking1(self, c):
        if self.s0[c-1] == 1:
            print("******1st Student has the last item, he completes the task and reports to teacher******\n\n")
            time.sleep(1.5)
        elif self.s1[c-1] == 1:
            print("******2nd Student has the last item, he completes the task and reports to teacher******\n")
            time.sleep(1.5)
        elif self.s2[c-1] == 1:
            print("******3rd Student has the last item, he completes the task and reports to teacher******\n")
            time.sleep(1.5)
        else:
            print("\nStudent having the corresponding last item has either completed his task\n")

    def table(self):
        with lock:
            a, b = 1, 2
            print("\n______Teacher places Pen and Paper on the shared table______\n")
            time.sleep(2)
            c = self.checking(a, b)
            self.checking1(c)

        with lock:
            a, b = 2, 3
            print("\n______Teacher places Question Paper and Paper on the shared table______\n")
            time.sleep(2)
            c = self.checking(a, b)
            self.checking1(c)

        with lock:
            a, b = 1, 3
            print("\n______Teacher places Pen and Question Paper on the shared table______\n")
            time.sleep(2)
            c = self.checking(a, b)
            self.checking1(c)

    def run(self):
        print("\nScene Illustration: \nThere are 3 student processes and 1 teacher process. Students are supposed to do their assignments and they need 3 things for that- pen, paper and question paper. The teacher has an infinite supply of all the three things. One student has pen, another has paper and another has question paper. The teacher places two things on a shared table and the student having the third complementary thing makes the assignment and tells the teacher on completion. The teacher then places two things out of three and again the student having the third thing makes the assignment and tells the teacher on completion. This cycle continues.\n\n")

        # Create threads for students
        t0 = threading.Thread(target=self.student0)
        t1 = threading.Thread(target=self.student1)
        t2 = threading.Thread(target=self.student2)

        t0.start()
        t0.join()
        t1.start()
        t1.join()
        t2.start()
        t2.join()

        # Teacher thread
        t_teacher = threading.Thread(target=self.table)
        t_teacher.start()
        t_teacher.join()

        print("\n\nScene 1 at Exam Hall is complete\n")
        try:
            a = int(input("\nHit 0 to enter other scene, else any to exit: "))
            if a == 0:
                return True
            else:
                self.exit_scene()
                return False
        except ValueError:
            self.exit_scene()
            return False

## Scene 2: Library Implementation
class LibraryScene:
    def __init__(self):
        self.exit_message = "\n\n\n\t Thank You. \nSubmitted To: \nMs. Anamika Arora. \n\n\nSubmitted By: \nSamarth Agarwal (Team Leader) G-1 \nKunwardeep Singh H-2 \nLakshaydeep Chaudhary K-2\n"

    def exit_scene(self):
        print(self.exit_message)
        time.sleep(2)
        sys.exit(0)

    def run(self):
        print("\nScene Illustration: \nTwo types of people can enter into a library-students and teachers. After entering the library, the visitor searches for the required books and get them. In order to get them issued, he goes to the single CPU which is there to process the issuing of books. Two types of queues are there at the counter-one for students and one for teachers. A student goes and stands at the tail of the queue for students and similarly the teacher goes and stands at the tail of the queue for teachers (FIFO). If a student is being served and a teacher arrives at the counter, he would be the next person to get service (PRIORITY - non preemptive). If two teachers arrive at the same time, they will stand in their queue to get service (FIFO).\n\n")

        try:
            n = int(input("Enter the number of persons: "))
            print("Enter the value 0 for teacher and 1 for student")
            
            persons = []
            priorities = []
            burst_times = []
            
            for i in range(n):
                persons.append(i+1)
                burst_times.append(1)
                priority = int(input(f"Who arrived {i+1}? = "))
                priorities.append(priority)
            
            # Sort based on priority (teachers first)
            for i in range(n):
                max_idx = i
                for j in range(i+1, n):
                    if priorities[j] < priorities[max_idx]:
                        max_idx = j
                
                # Swap priorities
                priorities[i], priorities[max_idx] = priorities[max_idx], priorities[i]
                # Swap burst times
                burst_times[i], burst_times[max_idx] = burst_times[max_idx], burst_times[i]
                # Swap person IDs
                persons[i], persons[max_idx] = persons[max_idx], persons[i]
            
            # Calculate waiting times
            waiting_times = [0] * n
            turnaround_times = [0] * n
            waiting_times[0] = 0
            
            for i in range(1, n):
                waiting_times[i] = burst_times[i-1] + waiting_times[i-1]
            
            for i in range(n):
                turnaround_times[i] = burst_times[i] + waiting_times[i]
            
            # Print results
            for i in range(n):
                print(f"\nWaiting time for {persons[i]} person is = {waiting_times[i]}")
            
            print("\n\nScene 2 at Library is complete\n")
            
            try:
                a = int(input("\nHit 0 to enter other scene, else any to exit: "))
                if a == 0:
                    return True
                else:
                    self.exit_scene()
                    return False
            except ValueError:
                self.exit_scene()
                return False
                
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            return False

## Scene 3: Optimized Library Implementation
class OptimizedLibraryScene:
    def __init__(self):
        self.exit_message = "\n\n\n\t Thank You. \nSubmitted To: \nMs. Anamika Arora. \n\n\nSubmitted By: \nSamarth Agarwal (Team Leader) G-1 \nKunwardeep Singh H-2 \nLakshaydeep Chaudhary K-2\n"

    def exit_scene(self):
        print(self.exit_message)
        time.sleep(2)
        sys.exit(0)

    def run(self):
        print("\nScene Illustration:\nIf two teachers arrive at the same time, they will stand in their queue to get service (FIFO).\n If a teacher is being served and during the period when he is being served, another teacher comes, then that teacher would get the service next. This process might continue leading to increase in waiting time of students and the program times to minimise this.\n\n")

        try:
            n = int(input("Enter the number of persons: "))
            print("Enter the value 0 for teacher and 1 for student")
            
            persons = []
            priorities = []
            burst_times = []
            teacher_count = 0
            student_priority_adjusted = False
            
            for i in range(n):
                persons.append(i+1)
                burst_times.append(1)
                priority = int(input(f"\t Who arrived {i+1}? = "))
                
                if priority == 0:  # Teacher
                    teacher_count += 1
                    if student_priority_adjusted:
                        priority += 1
                        student_priority_adjusted = False
                elif priority == 1 and teacher_count >= 3:
                    teacher_count = 0
                    student_priority_adjusted = True
                
                priorities.append(priority)
            
            # Sort based on priority (teachers first)
            for i in range(n):
                max_idx = i
                for j in range(i+1, n):
                    if priorities[j] < priorities[max_idx]:
                        max_idx = j
                
                # Swap priorities
                priorities[i], priorities[max_idx] = priorities[max_idx], priorities[i]
                # Swap burst times
                burst_times[i], burst_times[max_idx] = burst_times[max_idx], burst_times[i]
                # Swap person IDs
                persons[i], persons[max_idx] = persons[max_idx], persons[i]
            
            # Calculate waiting times
            waiting_times = [0] * n
            turnaround_times = [0] * n
            waiting_times[0] = 0
            
            for i in range(1, n):
                waiting_times[i] = burst_times[i-1] + waiting_times[i-1]
            
            for i in range(n):
                turnaround_times[i] = burst_times[i] + waiting_times[i]
            
            # Print results
            for i in range(n):
                print(f"\nWaiting time for person {persons[i]} is = {waiting_times[i]}")
            
            print("\n\nScene 3 at Library is complete\n")
            
            try:
                a = int(input("\nHit 0 to enter other scene, else any: "))
                if a == 0:
                    return True
                else:
                    self.exit_scene()
                    return False
            except ValueError:
                self.exit_scene()
                return False
                
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            return False

## Main Program
def main():
    print("***********************#  OS SIMULATION #***************************")
    print("\nThe following simulation involves THREE scenes.")
    print("SCENE 1: At Exam Hall")
    print("SCENE 2: At Library")
    print("SCENE 3: Optimized solution for the Library scenario")
    print("Please proceed accordingly by choosing one (1, 2, or 3): ", end="")
    
    try:
        scene_choice = int(input())
    except ValueError:
        print("Invalid input. Please enter 1, 2, or 3.")
        return
    
    while True:
        if scene_choice == 1:
            exam_hall = ExamHallScene()
            should_continue = exam_hall.run()
            if not should_continue:
                break
        elif scene_choice == 2:
            library = LibraryScene()
            should_continue = library.run()
            if not should_continue:
                break
        elif scene_choice == 3:
            optimized_library = OptimizedLibraryScene()
            should_continue = optimized_library.run()
            if not should_continue:
                break
        else:
            print("Scene doesn't match any of the listed, Have a Good Day!")
            time.sleep(2)
            break
        
        print("\nThe following simulation involves THREE scenes.")
        print("SCENE 1: At Exam Hall")
        print("SCENE 2: At Library")
        print("SCENE 3: Optimized solution for the Library scenario")
        print("Please proceed accordingly by choosing one (1, 2, or 3): ", end="")
        
        try:
            scene_choice = int(input())
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 3.")
            break

if __name__ == "__main__":
    main()