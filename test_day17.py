from collections import defaultdict
from unittest import TestCase

from numpy.ma.testutils import assert_equal
from sortedcontainers import SortedList

from day17 import dc, execute, parse, xlate


class Test(TestCase):
    def test_dc(self):
        assert_equal(dc(0, 997, 998, 999), 0)
        assert_equal(dc(1, 997, 998, 999), 1)
        assert_equal(dc(2, 997, 998, 999), 2)
        assert_equal(dc(3, 997, 998, 999), 3)
        assert_equal(dc(4, 997, 998, 999), 997)
        assert_equal(dc(5, 997, 998, 999), 998)
        assert_equal(dc(6, 997, 998, 999), 999)

    def test_parse(self):
        assert_equal(parse("Register A 997\nRegister B 998\nRegister C 999\nProgram 0,1,2,3,4,5,6,7"),
                     (997, 998, 999, [0, 1, 2, 3, 4, 5, 6, 7]))

    def test_operands(self):
        assert_equal(execute([2, 6], 0, 0, 9), (0, 1, 9, []))

        assert_equal(execute([5, 0, 5, 1, 5, 4], 10, 0, 0), (10, 0, 0, [0, 1, 2]))

        assert_equal(execute([0, 1, 5, 4, 3, 0], 2024, 0, 0),
                     (0, 0, 0, [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]))

        assert_equal(execute([1, 7], 0, 29, 0), (0, 26, 0, []))

        assert_equal(execute([4, 0], 0, 2024, 43690), (0, 44354, 43690, []))

    def test_find_register_a(self):
        pgm = [0, 3, 5, 4, 3, 0]
        out = []
        a = -1
        while out != pgm:
            a += 1
            _, _, _, out = execute(pgm, a, 0, 0)

        assert_equal(a, 117440)

    def test_quicklock(self):
        i = 0
        for n15 in range(8):
            a = assemble_a(n15)
            if execute(PGM, a, 0, 0)[3] != PGM[-1:]:
                continue
            for n14 in range(8):
                a = assemble_a(n15, n14)
                if execute(PGM, a, 0, 0)[3] != PGM[-2:]:
                    continue
                for n13 in range(8):
                    a = assemble_a(n15, n14, n13)
                    if execute(PGM, a, 0, 0)[3] != PGM[-3:]:
                        continue
                    for n12 in range(8):
                        a = assemble_a(n15, n14, n13, n12)
                        if execute(PGM, a, 0, 0)[3] != PGM[-4:]:
                            continue
                        for n11 in range(8):
                            a = assemble_a(n15, n14, n13, n12, n11)
                            if execute(PGM, a, 0, 0)[3] != PGM[-5:]:
                                continue
                            for n10 in range(8):
                                a = assemble_a(n15, n14, n13, n12, n11, n10)
                                if execute(PGM, a, 0, 0)[3] != PGM[-6:]:
                                    continue
                                for n9 in range(8):
                                    a = assemble_a(n15, n14, n13, n12, n11, n10, n9)
                                    if execute(PGM, a, 0, 0)[3] != PGM[-7:]:
                                        continue
                                    for n8 in range(8):
                                        a = assemble_a(n15, n14, n13, n12, n11, n10, n9, n8)
                                        if execute(PGM, a, 0, 0)[3] != PGM[-8:]:
                                            continue
                                        for n7 in range(8):
                                            a = assemble_a(n15, n14, n13, n12, n11, n10, n9, n8, n7)
                                            if execute(PGM, a, 0, 0)[3] != PGM[-9:]:
                                                continue
                                            for n6 in range(8):
                                                a = assemble_a(n15, n14, n13, n12, n11, n10, n9, n8, n7, n6)
                                                if execute(PGM, a, 0, 0)[3] != PGM[-10:]:
                                                    continue
                                                for n5 in range(8):
                                                    a = assemble_a(n15, n14, n13, n12, n11, n10, n9, n8, n7, n6, n5)
                                                    if execute(PGM, a, 0, 0)[3] != PGM[-11:]:
                                                        continue
                                                    for n4 in range(8):
                                                        a = assemble_a(n15, n14, n13, n12, n11, n10, n9, n8, n7, n6, n5,
                                                                       n4)
                                                        if execute(PGM, a, 0, 0)[3] != PGM[-12:]:
                                                            continue
                                                        for n3 in range(8):
                                                            a = assemble_a(n15, n14, n13, n12, n11, n10, n9, n8, n7, n6,
                                                                           n5, n4, n3)
                                                            if execute(PGM, a, 0, 0)[3] != PGM[-13:]:
                                                                continue
                                                            for n2 in range(8):
                                                                a = assemble_a(n15, n14, n13, n12, n11, n10, n9, n8, n7,
                                                                               n6, n5, n4, n3, n2)
                                                                if execute(PGM, a, 0, 0)[3] != PGM[-14:]:
                                                                    continue
                                                                for n1 in range(8):
                                                                    a = assemble_a(n15, n14, n13, n12, n11, n10, n9, n8,
                                                                                   n7, n6, n5, n4, n3, n2, n1)
                                                                    if execute(PGM, a, 0, 0)[3] != PGM[-15:]:
                                                                        continue
                                                                    for n0 in range(8):
                                                                        a = assemble_a(n15, n14, n13, n12, n11, n10, n9,
                                                                                       n8, n7, n6, n5, n4, n3, n2, n1,
                                                                                       n0)
                                                                        if execute(PGM, a, 0, 0)[3] != PGM:
                                                                            continue
                                                                        print(f'Part 1: {a}')
                                                                        return
        self.fail('No solution found')

    def test_lockpick(self):
        i = 0
        for n15 in prefixes[15]:
            for n14 in prefixes[14]:
                # if n14 >> 3 != n15 & 0o07:
                #     continue
                for n13 in prefixes[13]:
                    # if n13 >> 3 != n14 & 0o07:
                    #     continue
                    for n12 in prefixes[12]:
                        # if n12 >> 3 != n13 & 0o07:
                        #     continue
                        for n11 in prefixes[11]:
                            # if n11 >> 3 != n12 & 0o07:
                            #     continue
                            for n10 in prefixes[10]:
                                # if n10 >> 3 != n11 & 0o07:
                                #     continue
                                for n9 in prefixes[9]:
                                    # if n9 >> 3 != n10 & 0o07:
                                    #     continue
                                    for n8 in prefixes[8]:
                                        # if n8 >> 3 != n9 & 0o07:
                                        #     continue
                                        for n7 in prefixes[7]:
                                            # if n7 >> 3 != n8 & 0o07:
                                            #     continue
                                            for n6 in prefixes[6]:
                                                # if n6 >> 3 != n7 & 0o07:
                                                #     continue
                                                for n5 in prefixes[5]:
                                                    # if n5 >> 3 != n6 & 0o07:
                                                    #     continue
                                                    for n4 in prefixes[4]:
                                                        # if n4 >> 3 != n5 & 0o07:
                                                        #     continue
                                                        for n3 in prefixes[3]:
                                                            # if n3 >> 3 != n4 & 0o07:
                                                            #     continue
                                                            for n2 in prefixes[2]:
                                                                # if n2 >> 3 != n3 & 0o07:
                                                                #     continue
                                                                for n1 in prefixes[1]:
                                                                    # if n1 >> 3 != n2 & 0o07:
                                                                    #     continue
                                                                    for n0 in prefixes[0]:
                                                                        # if n0 >> 3 != n1 & 0o07:
                                                                        #     continue

                                                                        v = 0
                                                                        for a in [n15, n14, n13, n12, n11, n10, n9,
                                                                                  n8, n7,
                                                                                  n6, n5, n4, n3, n2, n1, n0]:
                                                                            v = v << 3
                                                                            v = v | (a & 0o07)
                                                                        _, _, _, out = execute(PGM, v, 0, 0)
                                                                        if out == PGM:
                                                                            print(f'Part 2: {a} -> {v}')
                                                                            return
                                                                        if i % 1000 == 0:
                                                                            print(f'{i=}, {a=}, {v=}, {out=}')
                                                                        i += 1

        self.fail('No solution found')

    def test_prefixes(self):
        potentials = defaultdict(SortedList)
        for i, p in enumerate(PGM):
            for a in range(0o1000):
                out = xlate(a, 0, 0)
                if out[0] == p:
                    potentials[i].add(a)
        for i in range(16):
            print(f'prefixes[{i}]=[' + ', '.join([f'0o{a:03o}' for a in potentials[i]]) + ']')

    def test_n15(self):
        print(xlate(105734774294938, 0, 0))


MGP = [0, 3, 5, 5, 3, 0, 6, 1, 3, 4, 5, 7, 5, 1, 4, 2]
PGM = [2, 4, 1, 5, 7, 5, 4, 3, 1, 6, 0, 3, 5, 5, 3, 0]
##### [2, 4, 1, 5, 7, 5, 4, 3, 1, 6, 0, 3, 5, 5, 3, 0]

prefixes = [[]] * 16
prefixes[0] = [0o001, 0o011, 0o040, 0o050, 0o060, 0o070, 0o076, 0o176, 0o201, 0o203, 0o211, 0o213, 0o223, 0o233, 0o243,
               0o253, 0o263, 0o273, 0o276, 0o376, 0o401, 0o411, 0o440, 0o450, 0o460, 0o470, 0o476, 0o576, 0o601, 0o602,
               0o611, 0o612, 0o622, 0o632, 0o642, 0o652, 0o662, 0o672, 0o676, 0o702, 0o712, 0o722, 0o732, 0o742, 0o752,
               0o762, 0o772, 0o776]
prefixes[1] = [0o016, 0o116, 0o141, 0o151, 0o216, 0o316, 0o340, 0o341, 0o350, 0o351, 0o360, 0o370, 0o403, 0o413, 0o416,
               0o423, 0o433, 0o443, 0o453, 0o463, 0o473, 0o516, 0o541, 0o551, 0o616, 0o716, 0o740, 0o741, 0o750, 0o751,
               0o760, 0o770]
prefixes[2] = [0o002, 0o012, 0o014, 0o022, 0o027, 0o032, 0o034, 0o042, 0o046, 0o052, 0o054, 0o061, 0o062, 0o067, 0o071,
               0o072, 0o074, 0o100, 0o102, 0o103, 0o110, 0o112, 0o113, 0o114, 0o120, 0o122, 0o123, 0o127, 0o130, 0o132,
               0o133, 0o134, 0o142, 0o143, 0o146, 0o152, 0o153, 0o154, 0o162, 0o163, 0o167, 0o172, 0o173, 0o174, 0o214,
               0o227, 0o234, 0o246, 0o254, 0o261, 0o267, 0o271, 0o274, 0o314, 0o327, 0o334, 0o346, 0o354, 0o367, 0o374,
               0o414, 0o427, 0o434, 0o446, 0o454, 0o461, 0o467, 0o471, 0o474, 0o500, 0o510, 0o514, 0o520, 0o527, 0o530,
               0o534, 0o546, 0o554, 0o567, 0o574, 0o614, 0o627, 0o634, 0o646, 0o654, 0o661, 0o667, 0o671, 0o674, 0o714,
               0o727, 0o734, 0o746, 0o754, 0o767, 0o774]
prefixes[3] = [0o004, 0o006, 0o007, 0o024, 0o044, 0o047, 0o064, 0o104, 0o106, 0o107, 0o124, 0o144, 0o147, 0o161, 0o164,
               0o171, 0o204, 0o206, 0o207, 0o224, 0o244, 0o247, 0o264, 0o300, 0o304, 0o306, 0o307, 0o310, 0o320, 0o324,
               0o330, 0o344, 0o347, 0o361, 0o364, 0o371, 0o404, 0o406, 0o407, 0o424, 0o444, 0o447, 0o464, 0o503, 0o504,
               0o506, 0o507, 0o513, 0o523, 0o524, 0o533, 0o543, 0o544, 0o547, 0o553, 0o561, 0o563, 0o564, 0o571, 0o573,
               0o604, 0o606, 0o607, 0o624, 0o644, 0o647, 0o664, 0o700, 0o704, 0o706, 0o707, 0o710, 0o720, 0o724, 0o730,
               0o744, 0o747, 0o761, 0o764, 0o771]
prefixes[4] = [0o017, 0o026, 0o057, 0o117, 0o121, 0o126, 0o131, 0o157, 0o200, 0o210, 0o217, 0o220, 0o226, 0o230, 0o257,
               0o317, 0o321, 0o326, 0o331, 0o357, 0o417, 0o426, 0o457, 0o517, 0o521, 0o526, 0o531, 0o557, 0o600, 0o610,
               0o617, 0o620, 0o626, 0o630, 0o657, 0o703, 0o713, 0o717, 0o721, 0o723, 0o726, 0o731, 0o733, 0o743, 0o753,
               0o757, 0o763, 0o773]
prefixes[5] = [0o004, 0o006, 0o007, 0o024, 0o044, 0o047, 0o064, 0o104, 0o106, 0o107, 0o124, 0o144, 0o147, 0o161, 0o164,
               0o171, 0o204, 0o206, 0o207, 0o224, 0o244, 0o247, 0o264, 0o300, 0o304, 0o306, 0o307, 0o310, 0o320, 0o324,
               0o330, 0o344, 0o347, 0o361, 0o364, 0o371, 0o404, 0o406, 0o407, 0o424, 0o444, 0o447, 0o464, 0o503, 0o504,
               0o506, 0o507, 0o513, 0o523, 0o524, 0o533, 0o543, 0o544, 0o547, 0o553, 0o561, 0o563, 0o564, 0o571, 0o573,
               0o604, 0o606, 0o607, 0o624, 0o644, 0o647, 0o664, 0o700, 0o704, 0o706, 0o707, 0o710, 0o720, 0o724, 0o730,
               0o744, 0o747, 0o761, 0o764, 0o771]
prefixes[6] = [0o016, 0o116, 0o141, 0o151, 0o216, 0o316, 0o340, 0o341, 0o350, 0o351, 0o360, 0o370, 0o403, 0o413, 0o416,
               0o423, 0o433, 0o443, 0o453, 0o463, 0o473, 0o516, 0o541, 0o551, 0o616, 0o716, 0o740, 0o741, 0o750, 0o751,
               0o760, 0o770]
prefixes[7] = [0o000, 0o005, 0o010, 0o015, 0o020, 0o021, 0o025, 0o030, 0o031, 0o035, 0o037, 0o045, 0o055, 0o065, 0o066,
               0o075, 0o077, 0o105, 0o115, 0o125, 0o135, 0o137, 0o145, 0o155, 0o165, 0o166, 0o175, 0o177, 0o205, 0o215,
               0o221, 0o225, 0o231, 0o235, 0o237, 0o245, 0o255, 0o265, 0o266, 0o275, 0o277, 0o303, 0o305, 0o313, 0o315,
               0o323, 0o325, 0o333, 0o335, 0o337, 0o343, 0o345, 0o353, 0o355, 0o363, 0o365, 0o366, 0o373, 0o375, 0o377,
               0o400, 0o402, 0o405, 0o410, 0o412, 0o415, 0o420, 0o421, 0o422, 0o425, 0o430, 0o431, 0o432, 0o435, 0o437,
               0o442, 0o445, 0o452, 0o455, 0o462, 0o465, 0o466, 0o472, 0o475, 0o477, 0o502, 0o505, 0o512, 0o515, 0o522,
               0o525, 0o532, 0o535, 0o537, 0o542, 0o545, 0o552, 0o555, 0o562, 0o565, 0o566, 0o572, 0o575, 0o577, 0o605,
               0o615, 0o621, 0o625, 0o631, 0o635, 0o637, 0o645, 0o655, 0o665, 0o666, 0o675, 0o677, 0o705, 0o715, 0o725,
               0o735, 0o737, 0o745, 0o755, 0o765, 0o766, 0o775, 0o777]
prefixes[8] = [0o002, 0o012, 0o014, 0o022, 0o027, 0o032, 0o034, 0o042, 0o046, 0o052, 0o054, 0o061, 0o062, 0o067, 0o071,
               0o072, 0o074, 0o100, 0o102, 0o103, 0o110, 0o112, 0o113, 0o114, 0o120, 0o122, 0o123, 0o127, 0o130, 0o132,
               0o133, 0o134, 0o142, 0o143, 0o146, 0o152, 0o153, 0o154, 0o162, 0o163, 0o167, 0o172, 0o173, 0o174, 0o214,
               0o227, 0o234, 0o246, 0o254, 0o261, 0o267, 0o271, 0o274, 0o314, 0o327, 0o334, 0o346, 0o354, 0o367, 0o374,
               0o414, 0o427, 0o434, 0o446, 0o454, 0o461, 0o467, 0o471, 0o474, 0o500, 0o510, 0o514, 0o520, 0o527, 0o530,
               0o534, 0o546, 0o554, 0o567, 0o574, 0o614, 0o627, 0o634, 0o646, 0o654, 0o661, 0o667, 0o671, 0o674, 0o714,
               0o727, 0o734, 0o746, 0o754, 0o767, 0o774]
prefixes[9] = [0o036, 0o101, 0o111, 0o136, 0o236, 0o240, 0o250, 0o260, 0o270, 0o301, 0o311, 0o336, 0o436, 0o501, 0o511,
               0o536, 0o603, 0o613, 0o623, 0o633, 0o636, 0o640, 0o643, 0o650, 0o653, 0o660, 0o663, 0o670, 0o673, 0o701,
               0o711, 0o736]
prefixes[10] = [0o003, 0o013, 0o023, 0o033, 0o041, 0o043, 0o051, 0o053, 0o056, 0o063, 0o073, 0o140, 0o150, 0o156, 0o160,
                0o170, 0o202, 0o212, 0o222, 0o232, 0o241, 0o242, 0o251, 0o252, 0o256, 0o262, 0o272, 0o302, 0o312, 0o322,
                0o332, 0o342, 0o352, 0o356, 0o362, 0o372, 0o441, 0o451, 0o456, 0o540, 0o550, 0o556, 0o560, 0o570, 0o641,
                0o651, 0o656, 0o756]
prefixes[11] = [0o000, 0o005, 0o010, 0o015, 0o020, 0o021, 0o025, 0o030, 0o031, 0o035, 0o037, 0o045, 0o055, 0o065, 0o066,
                0o075, 0o077, 0o105, 0o115, 0o125, 0o135, 0o137, 0o145, 0o155, 0o165, 0o166, 0o175, 0o177, 0o205, 0o215,
                0o221, 0o225, 0o231, 0o235, 0o237, 0o245, 0o255, 0o265, 0o266, 0o275, 0o277, 0o303, 0o305, 0o313, 0o315,
                0o323, 0o325, 0o333, 0o335, 0o337, 0o343, 0o345, 0o353, 0o355, 0o363, 0o365, 0o366, 0o373, 0o375, 0o377,
                0o400, 0o402, 0o405, 0o410, 0o412, 0o415, 0o420, 0o421, 0o422, 0o425, 0o430, 0o431, 0o432, 0o435, 0o437,
                0o442, 0o445, 0o452, 0o455, 0o462, 0o465, 0o466, 0o472, 0o475, 0o477, 0o502, 0o505, 0o512, 0o515, 0o522,
                0o525, 0o532, 0o535, 0o537, 0o542, 0o545, 0o552, 0o555, 0o562, 0o565, 0o566, 0o572, 0o575, 0o577, 0o605,
                0o615, 0o621, 0o625, 0o631, 0o635, 0o637, 0o645, 0o655, 0o665, 0o666, 0o675, 0o677, 0o705, 0o715, 0o725,
                0o735, 0o737, 0o745, 0o755, 0o765, 0o766, 0o775, 0o777]
prefixes[12] = [0o004, 0o006, 0o007, 0o024, 0o044, 0o047, 0o064, 0o104, 0o106, 0o107, 0o124, 0o144, 0o147, 0o161, 0o164,
                0o171, 0o204, 0o206, 0o207, 0o224, 0o244, 0o247, 0o264, 0o300, 0o304, 0o306, 0o307, 0o310, 0o320, 0o324,
                0o330, 0o344, 0o347, 0o361, 0o364, 0o371, 0o404, 0o406, 0o407, 0o424, 0o444, 0o447, 0o464, 0o503, 0o504,
                0o506, 0o507, 0o513, 0o523, 0o524, 0o533, 0o543, 0o544, 0o547, 0o553, 0o561, 0o563, 0o564, 0o571, 0o573,
                0o604, 0o606, 0o607, 0o624, 0o644, 0o647, 0o664, 0o700, 0o704, 0o706, 0o707, 0o710, 0o720, 0o724, 0o730,
                0o744, 0o747, 0o761, 0o764, 0o771]
prefixes[13] = [0o004, 0o006, 0o007, 0o024, 0o044, 0o047, 0o064, 0o104, 0o106, 0o107, 0o124, 0o144, 0o147, 0o161, 0o164,
                0o171, 0o204, 0o206, 0o207, 0o224, 0o244, 0o247, 0o264, 0o300, 0o304, 0o306, 0o307, 0o310, 0o320, 0o324,
                0o330, 0o344, 0o347, 0o361, 0o364, 0o371, 0o404, 0o406, 0o407, 0o424, 0o444, 0o447, 0o464, 0o503, 0o504,
                0o506, 0o507, 0o513, 0o523, 0o524, 0o533, 0o543, 0o544, 0o547, 0o553, 0o561, 0o563, 0o564, 0o571, 0o573,
                0o604, 0o606, 0o607, 0o624, 0o644, 0o647, 0o664, 0o700, 0o704, 0o706, 0o707, 0o710, 0o720, 0o724, 0o730,
                0o744, 0o747, 0o761, 0o764, 0o771]
prefixes[14] = [0o000, 0o005, 0o010, 0o015, 0o020, 0o021, 0o025, 0o030, 0o031, 0o035, 0o037, 0o045, 0o055, 0o065, 0o066,
                0o075, 0o077, 0o105, 0o115, 0o125, 0o135, 0o137, 0o145, 0o155, 0o165, 0o166, 0o175, 0o177, 0o205, 0o215,
                0o221, 0o225, 0o231, 0o235, 0o237, 0o245, 0o255, 0o265, 0o266, 0o275, 0o277, 0o303, 0o305, 0o313, 0o315,
                0o323, 0o325, 0o333, 0o335, 0o337, 0o343, 0o345, 0o353, 0o355, 0o363, 0o365, 0o366, 0o373, 0o375, 0o377,
                0o400, 0o402, 0o405, 0o410, 0o412, 0o415, 0o420, 0o421, 0o422, 0o425, 0o430, 0o431, 0o432, 0o435, 0o437,
                0o442, 0o445, 0o452, 0o455, 0o462, 0o465, 0o466, 0o472, 0o475, 0o477, 0o502, 0o505, 0o512, 0o515, 0o522,
                0o525, 0o532, 0o535, 0o537, 0o542, 0o545, 0o552, 0o555, 0o562, 0o565, 0o566, 0o572, 0o575, 0o577, 0o605,
                0o615, 0o621, 0o625, 0o631, 0o635, 0o637, 0o645, 0o655, 0o665, 0o666, 0o675, 0o677, 0o705, 0o715, 0o725,
                0o735, 0o737, 0o745, 0o755, 0o765, 0o766, 0o775, 0o777]
prefixes[15] = [0o003, 0o013, 0o023, 0o033, 0o041, 0o043, 0o051, 0o053, 0o056, 0o063, 0o073, 0o140, 0o150, 0o156, 0o160,
                0o170, 0o202, 0o212, 0o222, 0o232, 0o241, 0o242, 0o251, 0o252, 0o256, 0o262, 0o272, 0o302, 0o312, 0o322,
                0o332, 0o342, 0o352, 0o356, 0o362, 0o372, 0o441, 0o451, 0o456, 0o540, 0o550, 0o556, 0o560, 0o570, 0o641,
                0o651, 0o656, 0o756]


def assemble_a(*l):
    a = 0

    for v in l:
        a = a << 3
        a = a | v

    return a
