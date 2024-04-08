from pdfquery import PDFQuery
import csv
from fastapi import status


class Statement:
    def __init__(self, type):
        self.type = type

    def getStatement(self, pdfPath="", type="", filename=""):
        try:
            if pdfPath == "":
                return [
                    False, status.HTTP_400_BAD_REQUEST, "pdfPath cannot be empty"
                ]

            if type == "" or type not in ["cimb"]:
                return [
                    False, status.HTTP_400_BAD_REQUEST, "type is invalid"
                ]

            pdf = PDFQuery(pdfPath)
            pdf.load()

            # Use CSS-like selectors to locate the elements
            text_elements = pdf.pq('LTTextBoxHorizontal')

            date = []
            desc = []
            tempDesc = []
            money = []
            saldo = []
            sep = " "

            # with open('out.txt', 'r+') as f:
            for t in text_elements:
                t.text = t.text.strip()
                if t.text.lower() in ["", "tanggal", "deskripsi", "debit", "kredit", "saldo"]:
                    continue

                if "password" in t.text.lower() or "important" in t.text.lower() or "page" in t.text.lower():
                    continue

                if t.text != "":
                    if t._layout.x0 > 27 and t._layout.x1 < 85:  # date
                        date.append(t.text)
                        if len(tempDesc) > 0:
                            desc.append(sep.join(tempDesc))
                            tempDesc = []
                    elif t._layout.x0 > 102 and t._layout.x1 < 300:  # description
                        tempDesc.append(t.text)
                    # elif countToDebitOrCredit == 2 and isAfterDate:  # debit or credit
                    elif t._layout.x0 > 300 and t._layout.x1 < 480:  # debit or credit
                        money.append(float(t.text.replace(',', '')))
                    elif t._layout.x0 > 495 and t._layout.x1 < 600:  # saldo
                        saldo.append(float(t.text.replace(',', '')))
                # f.write(f"{t.text}||{t._layout.x0}||{t._layout.x1}\n")

            if len(tempDesc) > 0:
                desc.append(sep.join(tempDesc))

            if len(money) is not len(date) or len(money) is not len(desc) or len(money) is not len(saldo):
                return [
                    False, status.HTTP_400_BAD_REQUEST, "len error is not the same. money: {len(money)} date: {len(date)} desc: {len(desc)} saldo: {len(saldo)}"
                ]
                # print("len error is not the same")
                # print(
                #     f"money: {len(money)} date: {len(date)} desc: {len(desc)} saldo: {len(saldo)}")
                # exit(1)

            outPath = f"./output/{filename}.csv"
            with open(outPath, 'w', newline='') as file:
                writer = csv.writer(file)
                for i in range(len(money)):
                    # writer.writerow([date[i], desc[i], money[i], saldo[i]])
                    writer.writerow([date[i], desc[i], money[i]])

            return outPath
        except Exception as e:
            return [False, status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)]
