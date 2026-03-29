import re


class GeneratorAvSeats:
    def generate(self, data: str) -> list:
        result = []
        for test in data.split(","):
            template = r"\d+"
            template_letter = r"\w"
            a = re.findall(template, test)
            b = list(range(int(a[0]), int(a[1]) + 1))
            t = re.search(template_letter, test)
            [result.append(t.group() + str(x)) for x in b]
        return result

    def filter(self, data: list, seats: list) -> list:
        for s in seats:
            if s in data:
                data.remove(s)
        return data
