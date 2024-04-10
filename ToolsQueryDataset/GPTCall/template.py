from typing import Dict
class Combine_Template:
    system_prompt={
        
        "1":{"system":"下面会给到你一个functions定义，请基于给的functions定义，编辑5个会调用到它的自然语言中文问题和5个不会调用到它的自然语言中文问题。你要遵循以下几点要求：\n1.会调用到它的自然语言问题格式应该是：#TRUE#问题#调用functions的json格式#虚构的functions返回#\n2.不会调用到它的自然语言问题格式应该是：#FALSE#问题#\n3.除了共10条以上格式的数据，不要有任何其他的前置后置输出。\n4.请给出高质量的问题，且调用这个functions的问题场景很合理。如果你编辑的问题场景很合理，问题质量很高，你会获得200美元小费，如果数据质量很低，你会被Altman解雇"},
        
        "2":{"system":"下面会给到你两个functions定义，请基于给的functions定义，编辑5个会用到它们的自然语言中文问题和5个不会调用到它们的自然语言中文问题。你要遵循以下几点要求：\n1.会调用到它的自然语言问题格式应该是：#TRUE#问题#调用functions的json格式#虚构的functions返回#\n2.不会调用到它的自然语言问题格式应该是：#FALSE#问题#\n3.除了共10条以上格式的数据，不要有任何其他的前置后置输出。\n4.请给出高质量的问题，需要你编辑的问题场景能够合理去调用到这两个functions，如果给到的两个functions无法合理组合到一个问题场景中，则你可以减少问题场景中用到的functions数量。如果数据质量很高，你会获得200美元小费，如果数据质量很低，你会被Altman解雇"},
        
        "3":{"system":"下面会给到你三个functions定义，请基于给的functions定义，编辑5个会用到它们的自然语言中文问题和5个不会调用到它们的自然语言中文问题。你要遵循以下几点要求：\n1.会调用到它的自然语言问题格式应该是：#TRUE#问题#调用functions的json格式#虚构的functions返回#\n2.不会调用到它的自然语言问题格式应该是：#FALSE#问题#\n3.除了共10条以上格式的数据，不要有任何其他的前置后置输出。\n4.请给出高质量的问题，需要你编辑的问题场景能够合理去调用到这三个functions，如果给到的三个functions无法合理组合到一个问题场景中，则你可以减少问题场景中用到的functions数量。如果数据质量很高，你会获得200美元小费，如果数据质量很低，你会被Altman解雇"},
        
        "4":{"system":"下面会给到你四个functions定义，请基于给的functions定义，编辑5个会用到它们的自然语言中文问题和5个不会调用到它们的自然语言中文问题。你要遵循以下几点要求：\n1.会调用到它的自然语言问题格式应该是：#TRUE#问题#调用functions的json格式#虚构的functions返回#\n2.不会调用到它的自然语言问题格式应该是：#FALSE#问题#\n3.除了共10条以上格式的数据，不要有任何其他的前置后置输出。\n4.请给出高质量的问题，需要你编辑的问题场景能够合理去调用到这四个functions，如果给到的四个functions无法合理组合到一个问题场景中，则你可以减少问题场景中用到的functions数量。如果数据质量很高，你会获得200美元小费，如果数据质量很低，你会被Altman解雇"}           
    }
    @classmethod
    def generate_template(cls, system: Dict):
        return {'role':"system","content":system["system"]}
    @staticmethod
    def generate(new_message:str, value):
        messages=[]
        messages.append(Combine_Template.generate_template(Combine_Template.system_prompt[f'{value}']))
#         print(new_message)
        messages.append({"role":"user","content":f"{new_message}"})
        return messages
