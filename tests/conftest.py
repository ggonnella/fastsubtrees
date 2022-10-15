import pytest
import os
from array import array
from pathlib import Path

@pytest.fixture
def script():
  return lambda fn: Path(__file__).parent.parent / 'bin' / fn

@pytest.fixture
def ids_modules():
  return lambda fn: Path(__file__).parent.parent \
      / 'fastsubtrees' / 'ids_modules' / fn

@pytest.fixture
def testdata():
  return lambda fn: os.path.join(\
      os.path.join(os.path.dirname(__file__),"testdata/"), fn)

@pytest.fixture
def prebuilt():
  return lambda fn: os.path.join(\
      os.path.join(os.path.dirname(__file__),"prebuilt/"), fn)

@pytest.fixture
def testout():
  testoutdir = os.path.join(os.path.dirname(__file__),"testout/")
  if not os.path.exists(testoutdir):
    os.mkdir(testoutdir)
  return lambda fn: os.path.join(testoutdir, fn)

@pytest.fixture
def small_tree_file(testdata, testout):
  import fastsubtrees
  import fastsubtrees.ids_modules.ids_from_tabular_file as m
  generator = m.element_parent_ids(testdata("small_tree.tsv"))
  tree = fastsubtrees.Tree.construct(generator)
  tree.to_file(testout("small_tree.tree"))
  return testout("small_tree.tree")

@pytest.fixture
def results_query_small_tree_id_1():
  return array('Q', [1, 2, 8, 3, 7, 9, 4, 5])

@pytest.fixture
def results_query_small_tree_id_8():
  return array('Q', [8, 3, 7, 9, 4, 5])

@pytest.fixture
def results_query_small_tree_id_8_attrX():
   return "\n".join(['H', 'C, c', 'G', 'I', 'D', 'E'])

@pytest.fixture
def results_query_small_tree_id_8_attrX_after_add():
   return "\n".join(['H', 'None', 'C, c', 'G', 'None', 'None', 'None', \
          'None', 'None', 'None', 'I', 'D', 'E'])

@pytest.fixture
def results_query_small_tree_id_8_attrX_after_add2():
   return "\n".join(['H', 'F, X', 'C, c', 'G', 'TEN', 'TWELVE', 'None', \
           'ELEVEN', 'None', '13, 10+3', 'I', 'D', 'E'])

@pytest.fixture
def results_query_small_tree_id_8_add_subtree1():
  return array('Q', [8, 6, 3, 7, 9, 4, 5])

@pytest.fixture
def results_query_small_tree_id_8_add_subtree2():
  return array('Q', [8, 6, 3, 7, 10, 12, 15, 11, 14, 13, 9, 4, 5])

@pytest.fixture
def results_query_medium_tree_id_1():
  return array('Q', [1, 2, 4, 14, 58, 66, 162, 849, 170, 426, 769, 772, 243,
                     308, 395, 564, 263, 510, 167, 444, 472, 985, 452, 659, 527,
                     812, 940, 968, 307, 374, 983, 18, 19, 38, 83, 256, 572,
                     601, 996, 261, 323, 333, 945, 463, 509, 638, 838, 349,
                     922, 41, 492, 75, 474, 724, 373, 576, 21, 55, 181, 280,
                     516, 591, 926, 963, 583, 759, 814, 93, 130, 160, 220, 361,
                     404, 835, 455, 700, 773, 976, 920, 369, 850, 427, 525, 582,
                     625, 851, 861, 165, 189, 811, 346, 603, 696, 405, 860, 916,
                     420, 691, 276, 381, 592, 598, 133, 156, 250, 476, 880, 300,
                     530, 543, 557, 575, 33, 269, 397, 942, 46, 78, 110, 663,
                     939, 836, 955, 881, 235, 358, 451, 774, 755, 914, 91, 367,
                     549, 164, 974, 882, 270, 443, 632, 671, 664, 767, 800, 6,
                     67, 222, 281, 448, 697, 347, 847, 497, 137, 431, 522, 658,
                     640, 688, 900, 253, 259, 324, 362, 363, 641, 843, 845, 868,
                     783, 344, 887, 16, 188, 20, 60, 825, 62, 65, 81, 106, 116,
                     123, 217, 260, 356, 820, 757, 842, 441, 534, 645, 719, 971,
                     801, 247, 478, 844, 877, 602, 173, 617, 686, 141, 513, 190,
                     681, 490, 311, 588, 639, 864, 994, 329, 853, 736, 29, 45,
                     339, 350, 578, 949, 68, 99, 180, 262, 317, 377, 435, 826,
                     413, 682, 597, 765, 351, 703, 931, 203, 506, 507, 552, 600,
                     986, 97, 199, 213, 440, 743, 791, 519, 134, 150, 186, 352,
                     417, 871, 569, 782, 241, 550, 810, 271, 442, 540, 752, 545,
                     637, 828, 336, 372, 387, 400, 496, 512, 713, 822, 623, 355,
                     562, 630, 902, 888, 655, 957, 676, 746, 927, 804, 3, 5, 17,
                     25, 64, 73, 118, 305, 401, 321, 982, 456, 695, 803, 948,
                     331, 559, 965, 749, 147, 342, 571, 806, 763, 185, 567, 993,
                     187, 786, 950, 230, 244, 689, 699, 701, 407, 23, 192, 503,
                     643, 799, 660, 28, 47, 59, 148, 201, 627, 214, 670, 834,
                     967, 1000, 466, 61, 288, 411, 518, 526, 788, 648, 103, 174,
                     299, 535, 766, 194, 393, 863, 903, 475, 568, 590, 650, 925,
                     207, 998, 277, 915, 306, 462, 969, 191, 325, 768, 398, 445,
                     524, 809, 502, 548, 787, 12, 13, 24, 135, 139, 539, 705,
                     414, 556, 716, 35, 40, 127, 193, 228, 234, 382, 684, 290,
                     368, 565, 318, 493, 960, 131, 211, 704, 152, 479, 657, 958,
                     744, 777, 100, 365, 396, 459, 43, 69, 340, 873, 345, 500,
                     467, 89, 126, 107, 314, 930, 119, 236, 285, 423, 460, 508,
                     636, 515, 245, 434, 718, 771, 388, 453, 410, 730, 886, 946,
                     952, 48, 95, 109, 125, 218, 309, 613, 883, 656, 248, 327,
                     335, 376, 482, 973, 677, 932, 970, 128, 154, 215, 709, 714,
                     723, 732, 966, 741, 891, 468, 547, 619, 206, 313, 402, 385,
                     489, 606, 683, 504, 615, 471, 651, 198, 268, 428, 438, 764,
                     731, 780, 928, 380, 72, 82, 149, 226, 389, 538, 607, 544,
                     406, 151, 223, 447, 742, 558, 573, 813, 870, 894, 698, 155,
                     529, 178, 392, 470, 117, 153, 997, 251, 258, 390, 488, 856,
                     473, 935, 254, 702, 866, 332, 921, 990, 182, 200, 265, 761,
                     553, 692, 274, 341, 370, 561, 610, 485, 678, 938, 599, 674,
                     862, 936, 15, 54, 74, 319, 328, 541, 980, 531, 196, 237,
                     594, 649, 694, 721, 910, 707, 959, 937, 875, 205, 275, 279,
                     793, 778, 907, 416, 644, 63, 77, 112, 184, 264, 422, 837,
                     917, 631, 232, 233, 978, 378, 574, 629, 740, 911, 841, 246,
                     337, 753, 989, 197, 384, 808, 715, 833, 282, 802, 859, 855,
                     892, 22, 26, 52, 79, 120, 161, 168, 175, 371, 517, 521,
                     673, 784, 865, 789, 312, 179, 183, 464, 533, 944, 604, 608,
                     905, 375, 832, 748, 879, 792, 797, 292, 685, 708, 991, 579,
                     661, 523, 53, 104, 115, 212, 399, 421, 706, 169, 171, 255,
                     750, 756, 981, 409, 195, 208, 854, 912, 302, 817, 224, 605,
                     972, 758, 304, 343, 596, 587, 113, 158, 542, 947, 450, 520,
                     827, 992, 668, 815, 830, 31, 505, 890, 39, 71, 163, 242,
                     593, 727, 514, 612, 654, 823, 846, 858, 231, 621, 867, 781,
                     433, 816, 546, 577, 975, 36, 469, 680, 717, 805, 848, 898,
                     904, 954, 76, 90, 102, 138, 360, 739, 869, 908, 962, 437,
                     229, 536, 794, 272, 357, 642, 204, 348, 819, 266, 334, 419,
                     436, 896, 157, 172, 722, 913, 585, 941, 961, 653, 796, 146,
                     586, 874, 7, 8, 9, 10, 11, 34, 80, 140, 425, 725, 760, 202,
                     298, 354, 461, 729, 840, 824, 857, 872, 618, 273, 293, 779,
                     379, 551, 616, 785, 432, 494, 439, 114, 122, 484, 995, 486,
                     142, 284, 364, 628, 884, 710, 979, 487, 177, 209, 249, 301,
                     666, 675, 751, 326, 44, 85, 622, 647, 977, 646, 821, 86,
                     105, 239, 330, 495, 829, 895, 87, 159, 449, 726, 733, 770,
                     776, 897, 987, 121, 210, 415, 424, 132, 225, 807, 918, 291,
                     554, 555, 634, 609, 408, 430, 30, 32, 42, 88, 595, 964,
                     108, 143, 227, 238, 295, 624, 988, 457, 633, 316, 984, 366,
                     560, 735, 737, 876, 923, 465, 537, 665, 754, 919, 711, 412,
                     580, 386, 511, 446, 221, 790, 589, 693, 49, 56, 566, 57,
                     98, 322, 481, 581, 614, 878, 359, 51, 297, 315, 391, 501,
                     747, 418, 672, 734, 795, 652, 690, 798, 136, 353, 383, 611,
                     933, 712, 775, 839, 738, 219, 394, 458, 669, 762, 899, 909,
                     956, 662, 745, 953, 852, 27, 70, 94, 289, 144, 267, 286,
                     403, 499, 687, 924, 296, 620, 929, 240, 278, 454, 889, 943,
                     37, 728, 50, 287, 885, 429, 84, 283, 563, 92, 145, 166,
                     303, 667, 901, 216, 257, 338, 294, 320, 480, 310, 999, 477,
                     532, 906, 934, 635, 498, 584, 528, 252, 831, 679, 893, 96,
                     124, 491, 626, 101, 111, 483, 720, 818, 129, 176, 570,
                     951])

@pytest.fixture
def results_query_medium_tree_id_8():
  return array('Q', [8, 9, 10, 11, 34, 80, 140, 425, 725, 760, 202, 298, 354,
                     461, 729, 840, 824, 857, 872, 618, 273, 293, 779, 379, 551,
                     616, 785, 432, 494, 439, 114, 122, 484, 995, 486, 142, 284,
                     364, 628, 884, 710, 979, 487, 177, 209, 249, 301, 666, 675,
                     751, 326, 44, 85, 622, 647, 977, 646, 821, 86, 105, 239,
                     330, 495, 829, 895, 87, 159, 449, 726, 733, 770, 776, 897,
                     987, 121, 210, 415, 424, 132, 225, 807, 918, 291, 554, 555,
                     634, 609, 408, 430, 30, 32, 42, 88, 595, 964, 108, 143,
                     227, 238, 295, 624, 988, 457, 633, 316, 984, 366, 560, 735,
                     737, 876, 923, 465, 537, 665, 754, 919, 711, 412, 580, 386,
                     511, 446, 221, 790, 589, 693, 49, 56, 566, 57, 98, 322,
                     481, 581, 614, 878, 359])

@pytest.fixture
def results_query_medium_tree_id_566():
  return array('Q', [566])

@pytest.fixture
def results_add_subtree_small_subtree_1():
  return array('Q', [1, 2, 8, 6, 3, 7, 9, 4, 5])

@pytest.fixture
def results_add_subtree_medium_subtree_46():
  return array('Q', [46, 1002, 78, 110, 663, 939, 836, 955, 881, 235, 358,
                     451, 774, 755, 914, 91, 367, 549, 164, 974, 882])

@pytest.fixture
def results_delete_subtree_small_tree_id_1():
  return array('Q', [1, 2, 8, 4, 5])

@pytest.fixture
def results_delete_subtree_medium_tree_id_78():
  return array('Q', [46, 91, 367, 549, 164, 974, 882])
