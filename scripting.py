from random import choice


class Script:
    def __init__(self, path: str):
        self.path = path
        with open(self.path, encoding="UTF8") as txt_lines:
            self.old_txt = txt_lines.readlines()
        self.txt = [i.strip() for i in self.old_txt]

    def unpack(self, choice=None):
        if choice is None:
            return self.txt
        elif choice == "a":
            self.txt.sort()
            return self.txt
        elif choice == "d":
            self.txt.sort()
            self.txt.reverse()
            return self.txt
        elif choice == "dp":
            extra_list = []
            for i in self.txt:
                if i not in extra_list:
                    extra_list.append(i)
            return extra_list

    def release_one(self):
        return choice(self.txt)
