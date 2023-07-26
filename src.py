class typedb_schema_builder:
    schema=""
    context="?#"
    
    def __init__(self) -> None:
        self.schema="define"

    def abstract(self,type: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\tabstract;"
        else:
            self.context=type
            self.schema+="\n"+type+"abstract;"

    def sub(self,subtype,type: str):
        self.context=subtype
        self.schema+= "\n"+subtype+" sub "+type+";"

    def owns(self,type: str,owns: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\towns "+owns+";"   
        else:
            self.context=type
            self.schema+= "\n"+type+" owns "+owns+";"

    def owns_as(self,type: str,to_own: str,from_own: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\towns "+to_own+" as "+from_own+";"
        else:
            self.context=type
            self.schema+= "\n"+type+" owns "+to_own+" as "+from_own+";"

    def relates(self,type: str,role: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\trelates "+role+";"
        else:
            self.context=type
            self.schema+="\n"+type+" relates "+role+";"

    def relates_as(self,type,to_role: str,from_role: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\towns "+to_role+" as "+from_role+";"
        else:
            self.context=type
            self.schema+= "\n"+type+" owns "+to_role+" as "+from_role+";"

    def plays(self,type: str,relation: str,role: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\tplays "+relation+":"+role+";"
        else:
            self.context=type
            self.schema+= "\n"+type+" plays "+relation+":"+role+";"

    def plays_as(self,type: str,to_role: str,from_role: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\towns "+to_role+" as "+from_role+";"
        else:
            self.context=type
            self.schema+= "\n"+type+" owns "+to_role+" as "+from_role+";"

    def value(self,type: str,value: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\tvalue "+value+";"
        else:
            self.context=type
            self.schema+="\n"+type+" value "+value+";"

    def regex(self,type: str,regex: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\tregex \""+regex+"\";"
        else:
            self.context=type
            self.schema+="\n"+type+" regex \""+regex+"\";"

    def key(self,type: str,attribute: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\towns "+attribute+" @key;"
        else:
            self.context=type
            self.schema+="\n"+type+" owns "+attribute+" @key;"
        
    def unique(self,type: str,attribute: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\towns "+attribute+" @unique;"
        else:
            self.context=type
            self.schema+="\n"+type+" owns "+attribute+" @unique;"
        
    def get_schema(self):
        print(self.schema)
        return self.schema

    # Non user methods
    def exception(self):
        pass
