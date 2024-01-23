import numpy as np
import functions

from scipy.ndimage import label
from math import sqrt
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QFileDialog

import params


class BackEnd:
    def __init__(self, browser, image_win):
        self.browser = browser
        self.image_window = image_win

        self.adjacent_pix = None

        # adjacents
        self.type1 = []
        self.type1_num = 0

        self.type2 = []
        self.type2_num = 0

        self.type3 = []
        self.type3_num = 0

        self.type4 = []
        self.type4_num = 0

        self.type5 = []
        self.type5_num = 0

        self.rows_columns_test = True

    def clean_data(self):
        self.type1 = []
        self.type1_num = 0

        self.type2 = []
        self.type2_num = 0

        self.type3 = []
        self.type3_num = 0

        self.type4 = []
        self.type4_num = 0

        self.type5 = []
        self.type5_num = 0

        self.image_window.pix_splited = []
        self.image_window.pixels_splitted = []
        self.image_window.failed_pixels = []
        self.image_window.red_dots = []

        self.image_window.area0_count = [0] * 6
        self.image_window.areaA_count = [0] * 6
        self.image_window.areaB_count = [0] * 6
        self.image_window.areaC_count = [0] * 6

        self.image_window.pass_fail_label.setText("Pass")
        self.image_window.pass_fail_label.setHidden(True)  # Set the label as hidden initially

    def get_image_file(self):
        fname = QFileDialog.getOpenFileName(self.browser, 'Open file', 'c:\\', "Image files (*.jpg *.gif)")
        self.image_window.image_fname = fname[0]

    def get_pix_file(self):
        fname = QFileDialog.getOpenFileName(self.browser, 'Open file', 'c:\\', "Text files (*.txt)")
        self.image_window.pix_fname = fname[0]

    def start_app(self):
        self.clean_data()
        self.read_pix_file()
        self.find_dead_pixels()
        self.perform_AJ_tests()

        self.update_red_dots()  # purely for painting the red dots
        self.image_window.update()  # update new changes
        # self.check_group_in_area()

        self.image_window.show()

    def update_red_dots(self):
        self.image_window.red_dots.extend((x, y) for group in self.type1 for (x, y) in group)
        self.image_window.red_dots.extend((x, y) for group in self.type2 for (x, y) in group)
        self.image_window.red_dots.extend((x, y) for group in self.type3 for (x, y) in group)
        self.image_window.red_dots.extend((x, y) for group in self.type4 for (x, y) in group)
        self.image_window.red_dots.extend((x, y) for group in self.type5 for (x, y) in group)

        # self.image_window.red_dots.append([(x, y) for (x, y) in self.type1])
        # self.image_window.red_dots.append([(x, y) for (x, y) in self.type2])
        # self.image_window.red_dots.append([(x, y) for (x, y) in self.type3])
        # self.image_window.red_dots.append([(x, y) for (x, y) in self.type4])
        # self.image_window.red_dots.append([(x, y) for (x, y) in self.type5])

    def is_mostly_inside(self, points, region):
        """
        checks for each point in array (points)
        if region contains it
        return True/False
        """

        inside_count = 0

        # Check each point
        for x, y in points:
            p = QPoint(x, y)
            if region.contains(p):
                inside_count += 1

        # Check if most points are inside the region
        # print(f"{inside_count} > {len(points)} / 2 = {inside_count > len(points) / 2}")
        return inside_count > len(points) / 2

    def AJ_test(self, pixels, num):
        """
        function receives pixel array (for each adjacent type)
        for each group, check what area it belongs to
        update area_group counters arrays in the correct elements
        * meaning type4 adjacents in areaA will do areaA[4] += 1
        (areaX[num] += 1)
        """

        # braking to make extra sure on group doesn't count in two areas
        for group in pixels:
            if self.is_mostly_inside(group, self.image_window.r0):
                self.image_window.area0_count[num] += 1
                continue

            elif self.is_mostly_inside(group, self.image_window.rA):
                self.image_window.areaA_count[num] += 1
                continue

            elif self.is_mostly_inside(group, self.image_window.rB):
                self.image_window.areaB_count[num] += 1
                continue

            elif self.is_mostly_inside(group, self.image_window.rC):
                self.image_window.areaC_count[num] += 1
                continue

        # Ben Brownstain wanted this shit
        self.image_window.areaA_count[num] += self.image_window.area0_count[num]

    def perform_AJ_tests(self):
        tests_results = [True, True, True, True]  # contains results for pass/fail (True/False) for each adjacent type in all areas

        self.AJ_test(self.type1, 1)
        self.AJ_test(self.type2, 2)
        self.AJ_test(self.type3, 3)
        self.AJ_test(self.type4, 4)
        self.AJ_test(self.type5, 5)

        self.image_window.count_label0.setText(str(sum(self.image_window.area0_count)))
        self.image_window.count_labelA.setText(str(sum(self.image_window.areaA_count)))
        self.image_window.count_labelB.setText(str(sum(self.image_window.areaB_count)))
        self.image_window.count_labelC.setText(str(sum(self.image_window.areaC_count)))

        # I am so very sorry for this absolute garbage of a code
        for i in range(0, 5):
            if self.image_window.area0_count[i] > params.max_pixels0[i] and self.image_window.area0_count[i] != 0:
                tests_results[i] = False
                print(f"type{i}: {self.image_window.area0_count[i]} > {params.max_pixels0[i]}")
            if self.image_window.areaA_count[i] > params.max_pixelsA[i] and self.image_window.area0_count[i] != 0:
                tests_results[i] = False
                print(f"type{i}: {self.image_window.area0_count[i]} > {params.max_pixels0[i]}")

            if self.image_window.areaB_count[i] > params.max_pixelsB[i] and self.image_window.area0_count[i] != 0:
                tests_results[i] = False
                print(f"type{i}: {self.image_window.area0_count[i]} > {params.max_pixels0[i]}")

            if self.image_window.areaC_count[i] > params.max_pixelsC[i] and self.image_window.area0_count[i] != 0:
                tests_results[i] = False
                print(f"type{i}: {self.image_window.area0_count[i]} > {params.max_pixels0[i]}")


        if not tests_results[0]:
            self.image_window.area0_fill_label.setGeometry(self.image_window.r0.boundingRect())
            self.image_window.area0_fill_label.setText("")
            self.image_window.area0_fill_label.setStyleSheet("background-color: rgba(0, 255, 0, 40);")
            self.image_window.area0_fill_label.update()
            self.image_window.pass_fail_label.setText("Fail")

        if not tests_results[1]:
            self.image_window.areaA_l0.setGeometry(self.image_window.areaA_r0.boundingRect())
            self.image_window.areaA_l0.setStyleSheet("background-color: rgba(255,0,0, 40);")
            self.image_window.areaA_l0.update()

            self.image_window.areaA_l1.setGeometry(self.image_window.areaA_r1.boundingRect())
            self.image_window.areaA_l1.setStyleSheet("background-color: rgba(255, 0, 0, 40);")
            self.image_window.areaA_l1.update()

            self.image_window.areaA_l2.setGeometry(self.image_window.areaA_r2.boundingRect())
            self.image_window.areaA_l2.setStyleSheet("background-color: rgba(255, 0, 0, 40);")
            self.image_window.areaA_l2.update()

            self.image_window.areaA_l3.setGeometry(self.image_window.areaA_r3.boundingRect())
            self.image_window.areaA_l3.setStyleSheet("background-color: rgba(255, 0, 0, 40);")
            self.image_window.areaA_l3.update()
            self.image_window.pass_fail_label.setText("Fail")

        if not tests_results[2]:
            self.image_window.areaB_l0.setGeometry(self.image_window.areaB_r0.boundingRect())
            self.image_window.areaB_l0.setStyleSheet("background-color: rgba(255,255,0, 40);")
            self.image_window.areaB_l0.update()

            self.image_window.areaB_l1.setGeometry(self.image_window.areaB_r1.boundingRect())
            self.image_window.areaB_l1.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
            self.image_window.areaB_l1.update()

            self.image_window.areaB_l2.setGeometry(self.image_window.areaB_r2.boundingRect())
            self.image_window.areaB_l2.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
            self.image_window.areaB_l2.update()

            self.image_window.areaB_l3.setGeometry(self.image_window.areaB_r3.boundingRect())
            self.image_window.areaB_l3.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
            self.image_window.areaB_l3.update()
            self.image_window.pass_fail_label.setText("Fail")

        if not tests_results[3]:
            self.image_window.areaC_l0.setGeometry(self.image_window.areaC_r0.boundingRect())
            self.image_window.areaC_l0.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
            self.image_window.areaC_l0.update()

            self.image_window.areaC_l1.setGeometry(self.image_window.areaC_r1.boundingRect())
            self.image_window.areaC_l1.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
            self.image_window.areaC_l1.update()

            self.image_window.areaC_l2.setGeometry(self.image_window.areaC_r2.boundingRect())
            self.image_window.areaC_l2.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
            self.image_window.areaC_l2.update()

            self.image_window.areaC_l3.setGeometry(self.image_window.areaC_r3.boundingRect())
            self.image_window.areaC_l3.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
            self.image_window.areaC_l3.update()
            self.image_window.pass_fail_label.setText("Fail")

        if not self.rows_columns_test:
            self.image_window.pass_fail_label.setText("Fail")

        self.image_window.pass_fail_label.setHidden(False)

    # def check_group_in_area(self, group):
    #     for arr in self.image_window.red_dots:
    #         for (x, y) in arr:
    #             p = QPoint(x, y)
    #
    #             if self.image_window.r0.contains(p):
    #                 self.image_window.area0_count += 1
    #                 break
    #
    #             elif self.image_window.rA.contains(p):
    #                 self.image_window.areaA_count += 1
    #                 break
    #
    #             elif self.image_window.rB.contains(p):
    #                 self.image_window.areaB_count += 1
    #                 break
    #
    #             elif self.image_window.rC.contains(p):
    #                 self.image_window.areaC_count += 1
    #                 break
    #
    #     self.image_window.count_label0.setText(str(self.image_window.area0_count))
    #     self.image_window.count_labelA.setText(str(self.image_window.areaA_count))
    #     self.image_window.count_labelB.setText(str(self.image_window.areaB_count))
    #     self.image_window.count_labelC.setText(str(self.image_window.areaC_count))
    #
    #     # I am so very sorry for this absolute garbage of a code
    #     if self.image_window.area0_count > self.image_window.max_pixels0:
    #         self.image_window.area0_fill_label.setGeometry(self.image_window.r0.boundingRect())
    #         self.image_window.area0_fill_label.setText("")
    #         self.image_window.area0_fill_label.setStyleSheet("background-color: rgba(0, 255, 0, 40);")
    #         self.image_window.area0_fill_label.update()
    #
    #     if self.image_window.areaA_count > self.image_window.max_pixelsA:
    #         self.image_window.areaA_l0.setGeometry(self.image_window.areaA_r0.boundingRect())
    #         self.image_window.areaA_l0.setStyleSheet("background-color: rgba(255,0,0, 40);")
    #         self.image_window.areaA_l0.update()
    #
    #         self.image_window.areaA_l1.setGeometry(self.image_window.areaA_r1.boundingRect())
    #         self.image_window.areaA_l1.setStyleSheet("background-color: rgba(255, 0, 0, 40);")
    #         self.image_window.areaA_l1.update()
    #
    #         self.image_window.areaA_l2.setGeometry(self.image_window.areaA_r2.boundingRect())
    #         self.image_window.areaA_l2.setStyleSheet("background-color: rgba(255, 0, 0, 40);")
    #         self.image_window.areaA_l2.update()
    #
    #         self.image_window.areaA_l3.setGeometry(self.image_window.areaA_r3.boundingRect())
    #         self.image_window.areaA_l3.setStyleSheet("background-color: rgba(255, 0, 0, 40);")
    #         self.image_window.areaA_l3.update()
    #
    #     if self.image_window.areaB_count > self.image_window.max_pixelsB:
    #         self.image_window.areaB_l0.setGeometry(self.image_window.areaB_r0.boundingRect())
    #         self.image_window.areaB_l0.setStyleSheet("background-color: rgba(255,255,0, 40);")
    #         self.image_window.areaB_l0.update()
    #
    #         self.image_window.areaB_l1.setGeometry(self.image_window.areaB_r1.boundingRect())
    #         self.image_window.areaB_l1.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
    #         self.image_window.areaB_l1.update()
    #
    #         self.image_window.areaB_l2.setGeometry(self.image_window.areaB_r2.boundingRect())
    #         self.image_window.areaB_l2.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
    #         self.image_window.areaB_l2.update()
    #
    #         self.image_window.areaB_l3.setGeometry(self.image_window.areaB_r3.boundingRect())
    #         self.image_window.areaB_l3.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
    #         self.image_window.areaB_l3.update()
    #
    #     if self.image_window.areaC_count > self.image_window.max_pixelsC:
    #         self.image_window.areaC_l0.setGeometry(self.image_window.areaC_r0.boundingRect())
    #         self.image_window.areaC_l0.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
    #         self.image_window.areaC_l0.update()
    #
    #         self.image_window.areaC_l1.setGeometry(self.image_window.areaC_r1.boundingRect())
    #         self.image_window.areaC_l1.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
    #         self.image_window.areaC_l1.update()
    #
    #         self.image_window.areaC_l2.setGeometry(self.image_window.areaC_r2.boundingRect())
    #         self.image_window.areaC_l2.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
    #         self.image_window.areaC_l2.update()
    #
    #         self.image_window.areaC_l3.setGeometry(self.image_window.areaC_r3.boundingRect())
    #         self.image_window.areaC_l3.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
    #         self.image_window.areaC_l3.update()

    def find_dead_pixels(self):
        if not self.image_window.pixels_splitted:
            print('EMPTY')
            return

        # shape = functions.find_image_dimensions(self.image_window.image_fname)
        # shape = shape[::-1]

        self.type1, self.type1_num = self.find_adjacent_pixels(self.image_window.pixels_splitted, 2, 4)

        self.type2, self.type2_num = self.find_adjacent_pixels(self.image_window.pixels_splitted, 5, 6)

        self.type3, self.type3_num = self.find_adjacent_pixels(self.image_window.pixels_splitted, 7, 10)

        self.type4, self.type4_num = self.find_adjacent_pixels(self.image_window.pixels_splitted, 11, 16)

        self.type5, self.type5_num = self.find_adjacent_pixels(self.image_window.pixels_splitted, 17, 25)

        self.rows_columns_test = self.extract_rows_columns(self.image_window.pixels_splitted)

        # # linear distance calculation
        # for i, (x, y) in enumerate(self.image_window.pixels_splitted):
        #     for j, (x2, y2) in enumerate(self.image_window.pixels_splitted[:i]):
        #         if sqrt((x - x2) ** 2 + (y - y2) ** 2) <= sqrt(2):
        #             self.image_window.failed_pixels.append((x, y))

    def read_pix_file(self):
        try:
            f = open(self.image_window.pix_fname, "r")
            self.image_window.pix = f.readlines()
            self.image_window.pix = [i.replace(',', '') for i in self.image_window.pix]

            for line in self.image_window.pix:
                self.image_window.pix_splited = [int(s) for s in str.split(line) if s.isdigit()]
                self.image_window.pixels_splitted.append(self.image_window.pix_splited)

            # remove empty values and convert (y, x) to (x, y)
            self.image_window.pixels_splitted = list(
                filter(self.image_window.remove_empty, self.image_window.pixels_splitted))
            self.image_window.pixels_splitted = [(x, y) for (y, x) in self.image_window.pixels_splitted]

        except Exception as e:
            print(f"Error: {e}")
            self.image_window.pix = ""

    def find_adjacent_pixels(self, arr, min_group_size, max_group_size):
        # Directions for adjacent pixels (horizontal, vertical, diagonal)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Initialize visited set
        visited = set()

        # DFS function
        def dfs(pixel, group):
            x, y = pixel
            if pixel not in visited and pixel in arr:
                visited.add(pixel)
                group.append(pixel)
                for dx, dy in directions:
                    new_pixel = (x + dx, y + dy)
                    dfs(new_pixel, group)

        # Find all groups
        groups = []
        for pixel in arr:
            if pixel not in visited:
                group = []
                dfs(pixel, group)
                if min_group_size <= len(group) <= max_group_size:
                    groups.append(group)

        # Return all pixels individually
        # return [pixel for group in groups for pixel in group], len(groups)
        return [group for group in groups], len(groups)

    def extract_rows_columns(self, pixel_array):
        rows = [y for x, y in pixel_array]
        columns = [x for x, y in pixel_array]

        if len(rows) > params.ROW_LENGTH or len(columns) > params.COLUMN_LENGTH:
            return False  # test failed
        else:
            return True  # test passed

    # def find_dead_rows_and_columns(self, arr, num=1):
    #     # Initialize dictionaries to store pixel coordinates grouped by columns and rows
    #     columns = {}
    #     rows = {}
    #
    #     # Group pixel coordinates by columns and rows
    #     for x, y in arr:
    #         col_index = x // num
    #         row_index = y // num
    #
    #         # If the column index is not in the dictionary, add it
    #         if col_index not in columns:
    #             columns[col_index] = []
    #         # If the row index is not in the dictionary, add it
    #         if row_index not in rows:
    #             rows[row_index] = []
    #
    #         columns[col_index].append((x, y))
    #         rows[row_index].append((x, y))
    #
    #     return columns, rows
