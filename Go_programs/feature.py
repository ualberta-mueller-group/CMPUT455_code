import numpy as np
import os, sys
from board_base import coord_to_point, opponent, BLACK, WHITE, EMPTY, BORDER, PASS, NO_POINT, GO_POINT, board_array_size, DEFAULT_SIZE, full
from board import GoBoard
from gtp_connection import point_to_coord
from pattern import pat3set
from pattern_learn import patIndex
from pattern_util import PatternUtil
from typing import Dict, List, Tuple

NUM_SIMPLE_FEATURE = 26
FEATURES = Dict[GO_POINT,List[int]]

FeBasicFeatures = {
    "FE_PASS_NEW": 0,  # pass, previous move was not pass
    "FE_PASS_CONSECUTIVE": 1,  # pass, previous move was also pass
    "FE_CAPTURE": 2,  # String contiguous to new string in atari
    "FE_ATARI_KO": 3,  # Atari when there is a ko
    "FE_ATARI_OTHER": 4,  # Other atari
    "FE_SELF_ATARI": 5,
    "FE_LINE_1": 6,
    "FE_LINE_2": 7,
    "FE_LINE_3": 8,
    "FE_DIST_PREV_2": 9,  # d(dx,dy) = |dx|+|dy|+max(|dx|,|dy|)
    "FE_DIST_PREV_3": 10,
    "FE_DIST_PREV_4": 11,
    "FE_DIST_PREV_5": 12,
    "FE_DIST_PREV_6": 13,
    "FE_DIST_PREV_7": 14,
    "FE_DIST_PREV_8": 15,
    "FE_DIST_PREV_9": 16,
    "FE_DIST_PREV_OWN_0": 17,  #  play back in at same point after capture
    "FE_DIST_PREV_OWN_2": 18,
    "FE_DIST_PREV_OWN_3": 19,
    "FE_DIST_PREV_OWN_4": 20,
    "FE_DIST_PREV_OWN_5": 21,
    "FE_DIST_PREV_OWN_6": 22,
    "FE_DIST_PREV_OWN_7": 23,
    "FE_DIST_PREV_OWN_8": 24,
    "FE_DIST_PREV_OWN_9": 25,
}

# Load features weight
Features_weight = np.empty(shape=(0))
sys.path.insert(0, os.path.__file__)
dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, "features_weight.dat")
if os.path.isfile(filepath):
    sys.stderr.write("Load Features_weight from features_weight.dat ...")
    data = np.loadtxt(filepath)
    Features_weight = np.ones(len(data))
    for i in range(len(Features_weight)):
        Features_weight[i] = data[i][1]
else:
    print("No features weight file...")

patternWeightRec: Dict[int, List[int]] = {}

class Feature(object):

    lastBoardRec: list[int] = full(board_array_size(DEFAULT_SIZE), 
                                                 BORDER)

    @staticmethod
    def init_features(board: GoBoard) -> None:
        lastBoardRec = board.board.copy()
        
    @staticmethod
    def find_feature_name(feature_index: int) -> str:
        if feature_index >= NUM_SIMPLE_FEATURE:
            return ""
        for f in FeBasicFeatures:
            if FeBasicFeatures[f] == feature_index:
                return f
        return ""
        
    @staticmethod
    def write_mm_file(board: GoBoard, chosenMove: GO_POINT, filename: str) -> None:
        """
        Write file in a format as the mm learning tool requests.
        Please refer to Remi Coloum's website for the data format
        """
        with open(filename, "a") as f:
            assert chosenMove != NO_POINT
            features = Feature.find_all_features(board)
            f.write("#\n")
            data = []
            for fea in features[chosenMove]:
                data.append(f"{fea}")
            r = " ".join(data) + "\n"
            f.write(r)
            for m in features:
                data = []
                for fea in features[m]:
                    data.append(f"{fea}")
                r = " ".join(data) + "\n"
                f.write(r)
        f.close()

    @staticmethod
    def write_feature(features: FEATURES, point: GO_POINT) -> None:
    # TODO unused function, remove? Was this for a Dict?
        for f in features[point]:
            print(f, end=" ")

    @staticmethod
    def set_feature(features: FEATURES, point: GO_POINT, feature: int, 
                    callbypattern: bool = False) -> None:
        global patternWeightRec
        if point not in features:  # The move is not legal move
            return
        if feature not in features[point]:
            features[point].append(feature)
            if callbypattern:
                patternWeightRec[point].append(feature)

    @staticmethod
    def legal_moves_on_board(board: GoBoard) -> List[GO_POINT]:
        moves = board.get_empty_points()
        num_moves = len(moves)
        legalMoves = []
        for i in range(num_moves):
            if board.is_legal(moves[i], board.current_player):
                legalMoves.append(moves[i])
        return legalMoves

    @staticmethod
    def find_all_features(board: GoBoard) -> FEATURES:
        """
        Find all move's features on the board
        """
        global patternWeightRec
        legal_moves = Feature.legal_moves_on_board(board)
        features: FEATURES = {}
        features[PASS] = []
        for m in legal_moves:
            features[m] = []
        Feature.find_pass_features(features, board)
        Feature.find_full_board_features(features, board)
        Feature.find_dist_prev_move_features(features, board, legal_moves)
        Feature.find_line_pos_features(features, board, legal_moves)
        compare = (board.board != Feature.lastBoardRec)
        diff = np.sum(compare)
        # diffwhere=np.where(compare)
        #if 0 and diff == 0:
        #   for m in legal_moves:
        #       if m in patternWeightRec:
        #           for f in patternWeightRec[m]:
        #               if f not in features[m]:
        #                   features[m].append(f)
        #       else:
        #           patternWeightRec[m] = []
        #           Feature.find_pattern_feature(features, board, m)
        # elif(lastBoardRec!=[] and diff==1 and lastBoardRec[diffwhere]==0):
        #    pattern_checking_set = board.last_moves_empty_neighbors()
        #    for m in pattern_checking_set:
        #        patternWeightRec.pop(m,None)
        #    for m in legal_moves:
        #        if(m in pattern_checking_set):
        #            patternWeightRec[m]=[]
        #            Feature.find_pattern_feature(features, board, m)
        #        else:
        #            print('board',board.board)
        #            print('last',lastBoardRec)
        #            for f in patternWeightRec[m]:
        #                if f not in features[m]:
        #                    features[m].append(f)
        #        patternWeightRec[m]=[]
        #        Feature.find_pattern_feature(features, board, m)
        #    lastBoardRec=board.board.copy()
        #else:
        patternWeightRec.clear()
        patternWeightRec[PASS] = []
        for m in legal_moves:
            patternWeightRec[m] = []
            Feature.find_pattern_feature(features, board, m)
        Feature.lastBoardRec = board.board.copy()
        return features

    @staticmethod
    def find_move_feature(board: GoBoard, move: GO_POINT) -> List[int]:
        features = Feature.find_all_features(board)
        if move in features:
            return features[move]
        return []
        
    @staticmethod
    def find_pass_features(features: FEATURES, board: GoBoard) -> None:
        if board.last_move == PASS:
            Feature.set_feature(features, PASS, 
                                FeBasicFeatures["FE_PASS_CONSECUTIVE"])
        else:
            Feature.set_feature(features, PASS,
                                FeBasicFeatures["FE_PASS_NEW"])

    @staticmethod
    def find_self_atari_feature(features: FEATURES, board: GoBoard, point: GO_POINT) -> None:
        if PatternUtil.selfatari(board, point, board.current_player):
            Feature.set_feature(features, point,
                                FeBasicFeatures["FE_SELF_ATARI"])

    @staticmethod
    def find_pattern_feature(features: FEATURES, board: GoBoard, point: GO_POINT) -> None:
        p = PatternUtil.neighborhood_33(board, point)
        if p in pat3set:
            Feature.set_feature(features, point, 
                                patIndex[p] + NUM_SIMPLE_FEATURE, True)

    @staticmethod
    def find_block_anchors(board: GoBoard, limit: int) -> Tuple[List[GO_POINT], Dict[GO_POINT, List[GO_POINT]]]:
        """
        Find all blocks with liberty less or equal to limit on the board. Anchors is the smallest point in a block.
        Return a list of anchors and corresponding liberties
        Not efficient. One could maintain all blocks and anchors on the board, and update it when a move is played.
        """
        anchors: List[GO_POINT] = []
        liberty_dic: Dict[GO_POINT, List[GO_POINT]] = {}
        anchor_dic: Dict[GO_POINT, GO_POINT]  = {}

        for x in range(1, board.size + 1):
            for y in range(1, board.size + 1):
                point = coord_to_point(x, y, board.size)
                color = board.get_color(point)
                if point in anchor_dic:
                    continue
                if color != WHITE and color != BLACK:
                    continue
                liberty = 0
                the_libs = []
                group_points = [point]
                block_points = [point]
                min_index = point
                while group_points:
                    current_point = group_points.pop()
                    neighbors = board._neighbors(current_point)
                    for n in neighbors:
                        if n not in block_points:
                            if board.get_color(n) == BORDER:
                                continue
                            if board.get_color(n) == color:
                                group_points.append(n)
                                block_points.append(n)
                                if n < min_index:
                                    min_index = n
                            elif board.get_color(n) == EMPTY:
                                if n not in the_libs:
                                    the_libs.append(n)
                                    liberty += 1
                    if liberty > limit:
                        break
                for p in block_points:
                    anchor_dic[p] = min_index
                if liberty <= limit:
                    anchors.append(min_index)
                    liberty_dic[min_index] = the_libs

        return anchors, liberty_dic

    @staticmethod
    def find_full_board_features(features: FEATURES, board: GoBoard) -> None:
        anchors, liberty_dic = Feature.find_block_anchors(board, 2)
        for a in anchors:
            num_lib = len(liberty_dic[a])
            assert num_lib <= 2
            color = board.get_color(a)
            if (
                num_lib == 1 and opponent(board.current_player) == color
            ):  # find capture feature
                theLib = liberty_dic[a][0]
                Feature.find_capture_features(features, board, a, theLib)
            if (
                num_lib == 2 and opponent(board.current_player) == color
            ):  # find atari feature
                for l in liberty_dic[a]:
                    Feature.find_atari_features(features, board, a, l)

    @staticmethod
    def find_atari_features(features: FEATURES, board: GoBoard, 
                            anchor: GO_POINT, theLib: GO_POINT) -> None:
        # FE_ATARI_KO,            // Atari when there is a ko
        # FE_ATARI_OTHER,         // Other atari
        color = board.current_player
        opp_color = opponent(color)
        assert board._liberty(anchor, opp_color) == 2
        if board.ko_recapture != NO_POINT:
            Feature.set_feature(features, theLib, FeBasicFeatures["FE_ATARI_KO"])
        else:
            Feature.set_feature(features, theLib, FeBasicFeatures["FE_ATARI_OTHER"])

    @staticmethod
    def find_capture_features(features: FEATURES, board: GoBoard,
                              anchor: GO_POINT, theLib: GO_POINT) -> None:
        # TODO this is mostly commented out - does this code make sense?
        # FE_CAPTURE,   // String contiguous to new string in atari
        # f = None
        # our own neighbor is in atari
        f = FeBasicFeatures["FE_CAPTURE"]
        Feature.set_feature(features, theLib, f)

    @staticmethod
    def compute_feature(baseFeature: str, baseValue: int, value: int) -> int:
        return FeBasicFeatures[baseFeature] + value - baseValue

    @staticmethod
    def distance(board: GoBoard, p1: GO_POINT, p2: GO_POINT) -> int:
        assert p1 != NO_POINT
        assert p2 != NO_POINT
        row1, col1 = point_to_coord(p1, board.size)
        row2, col2 = point_to_coord(p2, board.size)
        dx = abs(col1 - col2)
        dy = abs(row1 - row2)
        return dx + dy + max(dx, dy)

    @staticmethod
    def distance_to_line(board: GoBoard, p: GO_POINT) -> int:
        halfSize = (board.size + 1) / 2
        row, col = point_to_coord(p, board.size)
        lineRow = board.size + 1 - row if row > halfSize else row
        lineCol = board.size + 1 - col if col > halfSize else col
        return min(lineRow, lineCol)

    @staticmethod
    def set_distance_last_move(features: FEATURES, board: GoBoard, 
                               legal_moves: List[GO_POINT]) -> None:
        for move in legal_moves:
            d = Feature.distance(board, move, board.last_move)
            assert d >= 2
            if d <= 9:
                fe = Feature.compute_feature("FE_DIST_PREV_2", 2, d)
                Feature.set_feature(features, move, fe)

    @staticmethod
    def set_distance_2nd_last_move(features: FEATURES, board: GoBoard, 
                                   legal_moves: List[GO_POINT]) -> None:
        for move in legal_moves:
            d = Feature.distance(board, move, board.last2_move)
            if d == 0:
                Feature.set_feature(
                    features, move, FeBasicFeatures["FE_DIST_PREV_OWN_0"]
                )
            elif d <= 9:
                assert d >= 2
                fe = Feature.compute_feature("FE_DIST_PREV_OWN_2", 2, d)
                Feature.set_feature(features, move, fe)
                # print(f"dist prew own {fe}")

    @staticmethod
    def find_dist_prev_move_features(features: FEATURES, board: GoBoard, 
                                     legal_moves: List[GO_POINT]) -> None:
        if board.last_move != NO_POINT:
            Feature.set_distance_last_move(features, board, legal_moves)
        if board.last2_move != NO_POINT:
            Feature.set_distance_2nd_last_move(features, board, legal_moves)

    @staticmethod
    def find_line_pos_features(features: FEATURES, board: GoBoard, 
                               legal_moves: List[GO_POINT]) -> None:
        for move in legal_moves:
            line = min(3, Feature.distance_to_line(board, move))
            f = Feature.compute_feature("FE_LINE_1", 1, line)
            assert f >= FeBasicFeatures["FE_LINE_1"]
            assert f <= FeBasicFeatures["FE_LINE_3"]
            Feature.set_feature(features, move, f)
            # print(f"dist line {f}")

    @staticmethod
    def compute_move_gamma(features_weight: np.ndarray, features: List[int]) -> float:
        gamma: float = 1.0
        for f in features:
            gamma = gamma * features_weight[f]
        return gamma
