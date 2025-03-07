import openai
import streamlit as st

# Configuramos nuestra API KEY
openai.api_key = 'tu-api-key-aqui'

# Creamos la funcion para generar la receta a partir de ingredientes, tipo de comida y tipo de dieta
def obtener_receta(ingredientes, tipo_comida, tipo_dieta):
    prompt = f"""
    Eres un chef experto en cocina internacional. Basándote en la lista de ingredientes proporcionada por el usuario, genera recetas detalladas, indicando los pasos a seguir, tiempos de cocción y recomendaciones adicionales. La receta debe ser clara, concisa y adecuada para cualquier persona, incluso sin experiencia en la cocina.
    Ingredientes: {ingredientes}
    Tipo de comida: {tipo_comida}
    Tipo de dieta: {tipo_dieta}
    """
    
    respuesta = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    
    receta = respuesta.choices[0].text.strip()
    return receta

# Creamos la funcion para la generacion de imagen de la receta con DALL·E
def obtener_imagen_receta(receta):
    prompt_imagen = f"Una imagen deliciosa de un plato de comida, representando la receta: {receta}. Imagen realista y atractiva para la comida."
    
    # Hacemos la llamada a la API de OpenAI para generar la imagen
    respuesta_imagen = openai.Image.create(
        prompt=prompt_imagen,
        n=1,
        size="1024x1024"
    )
    
    # Verificamos si la respuesta contiene la URL de la imagen
    url_imagen = respuesta_imagen['data'][0]['url']
    return url_imagen

# Configuramos la interfaz de Streamlit
st.title('GastronomIA 🍽️🤖')
st.write('Bienvenido a GastronomIA - Sabores inteligentes 🍳👨‍🍳\n\nUna aplicación web que genera recetas personalizadas basadas en los ingredientes que tienes disponibles. ¡Solo ingresa los ingredientes y el tipo de comida y deja que la IA te sorprenda con recetas deliciosas!')

# Aca voy a mostrar una imagen representativa estática antes de la generación de recetas
st.image('img/Ejemplo.jpg', caption='Imagen representativa de recetas', use_container_width=True)

# Entrada del prompt para ingredientes
ingredientes_usuario = st.text_area("Ingresa los ingredientes disponibles (separados por coma)")

# Selección de tipo de comida
tipo_comida = st.selectbox('Selecciona el tipo de comida', ['Desayuno', 'Almuerzo', 'Cena', 'Snack'])

# Selección de tipo de dieta
tipo_dieta = st.selectbox('Selecciona el tipo de dieta', ['Normal', 'Vegetariana', 'Vegana', 'Sin Gluten'])

# Y colocamos el boton que hace la magia :D
if st.button('Generar Receta'):
    if ingredientes_usuario:
        receta = obtener_receta(ingredientes_usuario, tipo_comida, tipo_dieta)
        st.write("### Receta recomendada:")
        st.write(receta)
        
        imagen_url = obtener_imagen_receta(receta)
        
        if imagen_url:
            st.write("### Imagen de la receta:")
            st.image(imagen_url, caption='Imagen representativa de la receta', use_container_width=True)
        else:
            st.error("No se pudo generar la imagen de la receta.")
    else:
        st.error("Por favor, ingresa al menos un ingrediente.")
