class Sos:
    def __init__(self):
        self.edad = 23
        self.travieso = True

    def di_algo(self): 
        print("Eres una puerca mi amor")

    def como_estas(self):
        if(self.travieso):
            print("\nando_travieso")
        else:
            print("bien bueno")

def main():
    s = Sos()
    s.di_algo()
    s.como_estas()


if __name__ == '__main__':
    main()
