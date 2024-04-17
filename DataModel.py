from pydantic import BaseModel

class DataModel(BaseModel):

	#Variables que permiten que la libreria pydantic haga el parseo entre 
	#el Json recibido y el modelo declarado

	Review: str


	# Esta función retorna los nombres de las columnas 
	# correspondietnes con el modelo exportado en joblib
	def columns(self):
		return['Review']