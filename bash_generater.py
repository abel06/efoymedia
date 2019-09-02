import re
class Generate():
    def __init__(self,inp):

        self.whileset=set(",ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ሀሁሂሂሄህሆለሉሊላሌልሎሏሐሑሒሓሔሕሖሗመሙሚማሜምሞሟሠሡሢሣሤሥሦሧረሩሪራሬርሮሯሰሱሲሳሴስሶሷሸሹሺሻሼሽሾሿቀቁቂቃቄቅቆቇቐቑቒቓቔቕቖበቡቢባቤብቦቧቨቩቪቫቬቭቮቯተቱቲታቴትቶቷቸቹቺቻቼችቾቿኀኁኂኃኄኅኆኇነኑኒናኔንኖኗኘኙኚኛኜኝኞኟአኡኢኣኤእኦኧከኩኪካኬክኮኯኸኹኺኻኼኽኾወዉዊዋዌውዎዐዑዒዓዔዕዖዘዙዚዛዜዝዞዟዠዡዢዣዤዥዦዧየዩዪያዬይዮዯደዱዲዳዴድዶዷጀዹዺዻዼዽዾዿጀጁጂጃጄጅጆጇገጉጊጋጌግጎጏጘጙጚጛጜጝጞጟጠጡጢጣጤጥጦጧጨጩጪጫጬጭጮጯጰጱጲጳጴጵጶጷጸጹጺጻጼጽጾጿፀፁፂፃፄፅፆፇፈፉፊፋፌፍፎፏፐፑፒፓፔፕፖፗቈቊቌቍቘቚቛቜቝኈኊኋኌኍኰኲኳኴኵዀዂዃዄዅጐጒጓጔጕፘፙፚ፩፪፫፬፭፮፯፰፱፲፳፴፵፶፷፸፹፺፻፼ ")
        self.tmp=""
        for i in  str(inp):
            if i in self.whileset:
                self.tmp+=i
            else:
                if i!=" ":
                    self.tmp+=" "
        self.b=self.tmp.split(",") 
        self.c=[]
        for val in self.b:
            self.tmp2=val.strip()
            self.d=re.sub(' +',u"\u0027" +","+ u"\u0027",self.tmp2)
            if self.d:
                self.c.append(self.d)
        self.m=str(self.c)
        self.m2=self.m[1:-1].replace('"',"'")
        self.result=self.m2.replace("', '","','")
        

    def get_bash(self):
        return str(self.result)