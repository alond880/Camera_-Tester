from datetime import datetime

import numpy as np
import cv2

from scipy.ndimage import label
from math import sqrt
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QFileDialog
from logger import Logger

import params


class BackEnd:
    def __init__(self, browser, image_win):
        self.browser = browser
        self.image_window = image_win
        self.logger = Logger()

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

        #  all groups in each area orginized by types
        self.area0_info = {"type1": [], "type1_count": 0, "type1_max_count": params.max_pixels0[0],
                           "type2": [], "type2_count": 0, "type2_max_count": params.max_pixels0[1],
                           "type3": [], "type3_count": 0, "type3_max_count": params.max_pixels0[2],
                           "type4": [], "type4_count": 0, "type4_max_count": params.max_pixels0[3],
                           "type5": [], "type5_count": 0, "type5_max_count": params.max_pixels0[4]
                           }
        self.areaA_info = {"type1": [], "type1_count": 0, "type1_max_count": params.max_pixelsA[0],
                           "type2": [], "type2_count": 0, "type2_max_count": params.max_pixelsA[1],
                           "type3": [], "type3_count": 0, "type3_max_count": params.max_pixelsA[2],
                           "type4": [], "type4_count": 0, "type4_max_count": params.max_pixelsA[3],
                           "type5": [], "type5_count": 0, "type5_max_count": params.max_pixelsA[4]
                           }
        self.areaB_info = {"type1": [], "type1_count": 0, "type1_max_count": params.max_pixelsB[0],
                           "type2": [], "type2_count": 0, "type2_max_count": params.max_pixelsB[1],
                           "type3": [], "type3_count": 0, "type3_max_count": params.max_pixelsB[2],
                           "type4": [], "type4_count": 0, "type4_max_count": params.max_pixelsB[3],
                           "type5": [], "type5_count": 0, "type5_max_count": params.max_pixelsB[4]
                           }
        self.areaC_info = {"type1": [], "type1_count": 0, "type1_max_count": params.max_pixelsC[0],
                           "type2": [], "type2_count": 0, "type2_max_count": params.max_pixelsC[1],
                           "type3": [], "type3_count": 0, "type3_max_count": params.max_pixelsC[2],
                           "type4": [], "type4_count": 0, "type4_max_count": params.max_pixelsC[3],
                           "type5": [], "type5_count": 0, "type5_max_count": params.max_pixelsC[4]
                           }

        self.rows_columns_test = True
        self.results_file_path = 'results.txt'
        self.pass_fail = True

    def start_app(self):
        self.clean_data()
        self.read_pix_file()
        self.find_dead_pixels()
        self.perform_AJ_counts()
        self.dripping_check()
        self.AJ_tests_final()

        self.update_red_dots()  # purely for painting the red dots
        self.update_circles()
        self.image_window.update()  # update new changes
        self.save_results()
        # self.check_group_in_area()

        self.image_window.show()

    def log_fail(self, area, counts):
        self.logger.log_info(f"Check failed: {area}")
        self.logger.log_info(
            f"Check failed: type1: {counts[0]}     type2: {counts[1]}     type3: {counts[2]}     type4: {counts[3]}     type5: {counts[4]}     ")
        # print(f"Check failed: {area}")
        # print(f"Check failed: type1: {counts[0]}     type2: {counts[1]}     type3: {counts[2]}     type4: {counts[3]}     type5: {counts[4]}     ")

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

        # 5 because there are 5 types
        self.image_window.area0_count = [0] * 5
        self.image_window.areaA_count = [0] * 5
        self.image_window.areaB_count = [0] * 5
        self.image_window.areaC_count = [0] * 5

        self.area0_info = {"type1": [], "type1_count": 0, "type1_max_count": params.max_pixels0[0],
                           "type2": [], "type2_count": 0, "type2_max_count": params.max_pixels0[1],
                           "type3": [], "type3_count": 0, "type3_max_count": params.max_pixels0[2],
                           "type4": [], "type4_count": 0, "type4_max_count": params.max_pixels0[3],
                           "type5": [], "type5_count": 0, "type5_max_count": params.max_pixels0[4]
                           }
        self.areaA_info = {"type1": [], "type1_count": 0, "type1_max_count": params.max_pixelsA[0],
                           "type2": [], "type2_count": 0, "type2_max_count": params.max_pixelsA[1],
                           "type3": [], "type3_count": 0, "type3_max_count": params.max_pixelsA[2],
                           "type4": [], "type4_count": 0, "type4_max_count": params.max_pixelsA[3],
                           "type5": [], "type5_count": 0, "type5_max_count": params.max_pixelsA[4]
                           }
        self.areaB_info = {"type1": [], "type1_count": 0, "type1_max_count": params.max_pixelsB[0],
                           "type2": [], "type2_count": 0, "type2_max_count": params.max_pixelsB[1],
                           "type3": [], "type3_count": 0, "type3_max_count": params.max_pixelsB[2],
                           "type4": [], "type4_count": 0, "type4_max_count": params.max_pixelsB[3],
                           "type5": [], "type5_count": 0, "type5_max_count": params.max_pixelsB[4]
                           }
        self.areaC_info = {"type1": [], "type1_count": 0, "type1_max_count": params.max_pixelsC[0],
                           "type2": [], "type2_count": 0, "type2_max_count": params.max_pixelsC[1],
                           "type3": [], "type3_count": 0, "type3_max_count": params.max_pixelsC[2],
                           "type4": [], "type4_count": 0, "type4_max_count": params.max_pixelsC[3],
                           "type5": [], "type5_count": 0, "type5_max_count": params.max_pixelsC[4]
                           }

        self.pass_fail = True

        self.image_window.pass_fail_label.setText("Pass")
        self.image_window.pass_fail_label.setHidden(True)  # Set the label as hidden initially

    def get_image_file(self):
        fname = QFileDialog.getOpenFileName(self.browser, 'Open file', 'c:\\', "Image files (*.jpg *.gif)")
        self.image_window.image_fname = fname[0]

    def get_pix_file(self):
        fname = QFileDialog.getOpenFileName(self.browser, 'Open file', 'c:\\', "Text files (*.txt)")
        self.image_window.pix_fname = fname[0]

    def update_red_dots(self):
        self.image_window.red_dots.extend((x, y) for group in self.type1 for (x, y) in group)
        self.image_window.red_dots.extend((x, y) for group in self.type2 for (x, y) in group)
        self.image_window.red_dots.extend((x, y) for group in self.type3 for (x, y) in group)
        self.image_window.red_dots.extend((x, y) for group in self.type4 for (x, y) in group)
        self.image_window.red_dots.extend((x, y) for group in self.type5 for (x, y) in group)

    def find_circle_coordinates(self, dots):
        min_x = min(dot[0] for dot in dots)
        max_x = max(dot[0] for dot in dots)
        min_y = min(dot[1] for dot in dots)
        max_y = max(dot[1] for dot in dots)

        # Calculate the center of the circle
        circle_center = ((min_x + max_x) / 2, (min_y + max_y) / 2)

        # Calculate the radius of the circle
        radius = max(max_x - min_x, max_y - min_y) / 2

        # Calculate the top-left corner of the rectangle containing the circle
        top_left_x = circle_center[0] - radius * params.CIRCLE_RAD_ENHANCE - len(dots) / 2
        top_left_y = circle_center[1] - radius * params.CIRCLE_RAD_ENHANCE - len(dots) / 2

        return top_left_x, top_left_y

    def update_circles(self):
        for group in self.type1:
            m = self.find_circle_coordinates(group)
            circle = {
                "center": (m[0], m[1]),
                "rad": len(group) * params.CIRCLE_RAD_ENHANCE,
                "color": params.TYPE1_COLOR
            }
            self.image_window.circles.append(circle)

        for group in self.type2:
            m = self.find_circle_coordinates(group)
            circle = {
                "center": (m[0], m[1]),
                "rad": len(group) * params.CIRCLE_RAD_ENHANCE,
                "color": params.TYPE2_COLOR
            }
            self.image_window.circles.append(circle)

        for group in self.type3:
            m = self.find_circle_coordinates(group)
            circle = {
                "center": (m[0], m[1]),
                "rad": len(group) * params.CIRCLE_RAD_ENHANCE,
                "color": params.TYPE3_COLOR
            }
            self.image_window.circles.append(circle)

        for group in self.type4:
            m = self.find_circle_coordinates(group)
            circle = {
                "center": (m[0], m[1]),
                "rad": len(group) * params.CIRCLE_RAD_ENHANCE,
                "color": params.TYPE4_COLOR
            }
            self.image_window.circles.append(circle)

        for group in self.type5:
            m = self.find_circle_coordinates(group)
            circle = {
                "center": (m[0], m[1]),
                "rad": len(group) * params.CIRCLE_RAD_ENHANCE,
                "color": params.TYPE5_COLOR
            }
            self.image_window.circles.append(circle)

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

    def AJ_count(self, pixels, type_num):
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
                self.image_window.area0_count[type_num] += 1
                self.area0_info["type" + str(type_num) + "_count"] += 1
                self.area0_info["type" + str(type_num)].append(group)
                continue

            elif self.is_mostly_inside(group, self.image_window.rA):
                self.image_window.areaA_count[type_num] += 1
                self.areaA_info["type" + str(type_num) + "_count"] += 1
                self.areaA_info["type" + str(type_num)].append(group)
                continue

            elif self.is_mostly_inside(group, self.image_window.rB):
                self.image_window.areaB_count[type_num] += 1
                self.areaB_info["type" + str(type_num) + "_count"] += 1
                self.areaB_info["type" + str(type_num)].append(group)
                continue

            elif self.is_mostly_inside(group, self.image_window.rC):
                self.image_window.areaC_count[type_num] += 1
                self.areaC_info["type" + str(type_num) + "_count"] += 1
                self.areaC_info["type" + str(type_num)].append(group)
                continue

        # Ben Brownstain wanted this shit
        # self.image_window.areaA_count[num] += self.image_window.area0_count[num]

    def perform_AJ_counts(self):
        self.AJ_count(self.type1, 1)
        self.AJ_count(self.type2, 2)
        self.AJ_count(self.type3, 3)
        self.AJ_count(self.type4, 4)
        self.AJ_count(self.type5, 5)

    def update_counts(self):
        try:
            for i in range(1, 6):
                self.image_window.area0_count[i - 1] = self.area0_info["type" + str(i) + "_count"]
                self.image_window.areaA_count[i - 1] = self.areaA_info["type" + str(i) + "_count"]
                self.image_window.areaB_count[i - 1] = self.areaB_info["type" + str(i) + "_count"]
                self.image_window.areaC_count[i - 1] = self.areaC_info["type" + str(i) + "_count"]

        except Exception as e:
            self.logger.log_exception(f"Update_counts: {e}")

    def dripping(self, area_info, origin_type, bigger_types, extra_groups_num):
        try:
            for type in bigger_types:  # for each type in the following types in the hierarchy
                while extra_groups_num > 0:  # there are extra groups
                    if area_info[type + "_max_count"] > area_info[type + "_count"]:  # if there is room in this type
                        #  transfer group
                        group = area_info[origin_type].pop(-1)
                        area_info[type].append(group)

                        # update counts
                        extra_groups_num -= 1
                        area_info[origin_type + "_count"] -= 1
                        area_info[type + "_count"] += 1
                    else:
                        break

                if type == "type5" and area_info[type + "_count"] <= area_info[type + "_max_count"]:
                    return False  # end of line, check failed

            return True  # check have been dripped

        except Exception as e:
            self.logger.log_error(f"Dripping: {e}")

    def dripping_check(self):
        types = ["type1", "type2", "type3", "type4", "type5"]

        for i in range(0, 5):
            if self.image_window.area0_count[i] > params.max_pixels0[i] != 0:
                self.dripping(self.area0_info, "type" + str(i), types[i:],
                              self.image_window.area0_count[i] - params.max_pixels0[i])

            if self.image_window.areaA_count[i] > params.max_pixelsA[i] != 0:
                self.dripping(self.areaA_info, "type" + str(i), types[i:],
                              self.image_window.areaA_count[i] - params.max_pixelsA[i])

            if self.image_window.areaB_count[i] > params.max_pixelsB[i] != 0:
                self.dripping(self.areaB_info, "type" + str(i), types[i:],
                              self.image_window.areaB_count[i] - params.max_pixelsB[i])

            if self.image_window.areaC_count[i] > params.max_pixelsC[i] != 0:
                self.dripping(self.areaC_info, "type" + str(i), types[i:],
                              self.image_window.areaC_count[i] - params.max_pixelsC[i])

        self.update_counts()

    def AJ_tests_final(self):
        tests_results = [True, True, True,
                         True]  # contains results for pass/fail (True/False) for each adjacent type in all areas

        # I am so very sorry for this absolute garbage of a code
        for i in range(0, 5):
            if self.image_window.area0_count[i] > params.max_pixels0[i] != 0:
                tests_results[i] = False
                self.pass_fail = False
                print(f"AREA 0 FAILED: area0_count[{i}]: {self.image_window.area0_count[i]} > {params.max_pixels0[i]}")

            if self.image_window.areaA_count[i] > params.max_pixelsA[i]:
                tests_results[i] = False
                self.pass_fail = False
                print(f"AREA A FAILED: areaA_count[{i}]: {self.image_window.areaA_count[i]} > {params.max_pixelsA[i]}")

            if self.image_window.areaB_count[i] > params.max_pixelsB[i]:
                tests_results[i] = False
                self.pass_fail = False
                print(f"AREA B FAILED: areaB_count[{i}]: {self.image_window.areaB_count[i]} > {params.max_pixelsB[i]}")

            if self.image_window.areaC_count[i] > params.max_pixelsC[i]:
                tests_results[i] = False
                self.pass_fail = False
                print(f"AREA C FAILED: areaC_count[{i}]: {self.image_window.areaC_count[i]} > {params.max_pixelsC[i]}")

        if not tests_results[0]:
            self.image_window.area0_fill_label.setGeometry(self.image_window.r0.boundingRect())
            self.image_window.area0_fill_label.setText("")
            self.image_window.area0_fill_label.setStyleSheet("background-color: rgba(0, 255, 0, 40);")
            self.image_window.area0_fill_label.update()
            self.image_window.pass_fail_label.setText("Fail")

            self.log_fail("area0", self.image_window.area0_count)

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

            self.log_fail("areaA", self.image_window.areaA_count)

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
            self.log_fail("areaB", self.image_window.areaB_count)

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
            self.log_fail("areaC", self.image_window.areaC_count)

        # if not self.rows_columns_test:
        #     self.image_window.pass_fail_label.setText("Fail")

        self.image_window.pass_fail_label.setHidden(False)

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

    def save_results(self):
        if self.pass_fail:
            test_str = "PASS"
        else:
            test_str = "FAIL"

        try:
            with open(self.results_file_path, "a") as file:
                file.write(str(datetime.now()) + "  TEST RESULT: " + test_str + "\n")

                file.write("AREA 0: \n")
                for i, val in enumerate(self.image_window.area0_count):
                    file.write(f"type{str(i+1)}: GROUP COUNT: {val}\n")

                file.write("AREA A: \n")
                for i, val in enumerate(self.image_window.areaA_count):
                    file.write(f"type{str(i+1)}: GROUP COUNT: {val}\n")

                file.write("AREA B: \n")
                for i, val in enumerate(self.image_window.areaB_count):
                    file.write(f"type{str(i+1)}: GROUP COUNT: {val}\n")

                file.write("AREA C: \n")
                for i, val in enumerate(self.image_window.areaC_count):
                    file.write(f"type{str(i+1)}: GROUP COUNT: {val}\n")



                file.write("-----------------------------------------------------------------\n")

        except Exception as e:
            self.logger.log_exception(f"Failed to save results:     {e}")

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
