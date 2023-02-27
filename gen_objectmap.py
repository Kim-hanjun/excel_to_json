import json
import argparse
import pandas as pd


# Depth 1~4가 그 전 행과 동일한지 비교. 다르다면 dict에 추가하는 방식

def main(args):
    json_list = []
    json_dict = {}
    data = pd.read_excel(args.excelfile_path, sheet_name="2022_객체맵개편안")
    # data.loc[64, "Depth 3"] = "범죄"
    # data.loc[[219, 220, 221, 222, 223, 224], "Depth 3"] = "일상 생활"
    # data.loc[[226, 227], "Depth 3"] = "악기 연주"
    # data.loc[[785, 786, 787, 788, 789], "Depth 3"] = "유제품"

    for i in range(1, len(data)):
        if data["Depth 1"][i] != data["Depth 1"][i - 1]:
            json_list.append(json_dict)
            json_dict = {"onelevel": data["Depth 1"][i]}
            json_dict["twolist"] = []

        if data["Depth 2"][i] != data["Depth 2"][i - 1]:
            json_dict_Depth2 = {"twolevel": data["Depth 2"][i]}
            json_dict["twolist"].append(json_dict_Depth2)
            if data["Depth 3"].isna()[i]:
                json_dict["twolist"][-1]["thrlist"] = None
                continue
            else:
                json_dict["twolist"][-1]["thrlist"] = []

        if data["Depth 3"][i] != data["Depth 3"][i - 1]:
            json_dict_Depth3 = {"thrlevel": data["Depth 3"][i]}
            json_dict["twolist"][-1]["thrlist"].append(json_dict_Depth3)
            if data["Depth 4"].isna()[i]:
                json_dict["twolist"][-1]["thrlist"][-1]["fourlist"] = None
                continue
            else:
                json_dict["twolist"][-1]["thrlist"][-1]["fourlist"] = []

        if data["Depth 4"][i] != data["Depth 4"][i - 1]:
            json_dict_Depth4 = {"fourlevel": data["Depth 4"][i]}
            json_dict["twolist"][-1]["thrlist"][-1]["fourlist"].append(json_dict_Depth4)
        i += 1

    # 처음에 append된 빈 딕셔너리 제거
    json_list.remove({})
    # 반복문이 끝나고 아직 append 되지 못했던 마지막 dict append
    json_list.append(json_dict)

    with open("modify_test_objectmap.json", "w", encoding="utf-8") as file:
        json.dump(json_list, file, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excelfile_path", type=str, default="./2022_NIA_AI허브_객체맵 개편 (0206최종본).xlsx")
    args = parser.parse_args()
    main(args)
