from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routes import inventory
from typing import List
from dotenv import load_dotenv
import os
from openai import OpenAI
from utils.inventory import load_inventory, filter_by_category, find_item_by_name, load_all_item_names
import json


# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FastAPI app initialization
app = FastAPI()

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Base route for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the ChatBot Backend!"}

# Include API routes
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])


def extract_intent_and_entities(user_message: str, context: list, inventory: list) -> dict:
    """
    Use OpenAI to extract intent and entities from the user's message.
    The possible intents are:
      - 'consulta_inventario'
      - 'consulta_general'
      - 'desconocido'
      - 'compra'
      - 'pedir_sugerencia'
    
    The possible entities to extract (if present) are:
      - 'category'
      - 'brand'
      - 'max_price'
      - 'product'
      - 'quantity'
        
    :param user_message: The message sent by the user.
    :param context: A list of previous conversation messages (each item is a dict with keys "role" and "content").
    :return: A dictionary containing the extracted intent and entities.
    """
    try:

        inventory_str = json.dumps(inventory, ensure_ascii=False, indent=2)
        
        system_prompt = (
            "Eres un asistente que analiza mensajes del usuario para identificar su intención y las entidades relevantes. "
            "Este es el inventario de la tienda:\n"
            f"{inventory_str}\n\n"
            "Devuelve la respuesta como un objeto JSON con los campos 'intent' y 'entities'. "
            "Las posibles intenciones son: 'consulta_inventario', 'consulta_general', 'desconocido', 'compra' o 'pedir_sugerencia'. "
            "La intención 'consulta_inventario' se usa si el usuario pregunta por productos que podrían estar en el inventario. "
            "'consulta_general' se usa si el usuario pregunta por algo ajeno al inventario. "
            "'desconocido' se usa si la consulta no es comprensible. "
            "'compra' se usa si el usuario desea comprar un producto directamente. "
            "'pedir_sugerencia' se usa si el usuario pide una recomendación o sugerencia de productos. "
            "'descripcion' se usa si el usuario pregunta por la descripción de un producto en especifico. "
            "\n\nLas posibles entidades a extraer son: 'category', 'brand', 'max_price', 'product' y 'quantity'. "
            "Devuélvelas solo si existen en el texto del usuario, ajustándolas a valores lógicos basados en el inventario si es posible. "
            "Un ejemplo de respuesta JSON:\n\n"
            "{\n"
            "  \"intent\": \"consulta_inventario\",\n"
            "  \"entities\": {\n"
            "    \"category\": \"alimentos\",\n"
            "    \"max_price\": 100,\n"
            "    \"brand\": \"Coca Cola\",\n"
            "    \"product\": \"refresco\",\n"
            "    \"quantity\": 2\n"
            "  }\n"
            "}\n\n"
            "Si no hay entidades, envía un objeto vacío para 'entities'. "
            "Asegúrate de que la respuesta sea JSON válido, sin texto adicional."
        )

        # Llamada a la API de OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context + [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.0,
            max_tokens=200
        )

        # Obtenemos la respuesta
        extracted_data = response.choices[0].message.content.strip()
        
        # Parseamos la respuesta como JSON
        return json.loads(extracted_data)

    except json.JSONDecodeError as e:
        print(f"Error al analizar la respuesta de OpenAI: {e}")
        return {"intent": "desconocido", "entities": {}}
    except Exception as e:
        print(f"Error extrayendo intención y entidades: {e}")
        return {"intent": "desconocido", "entities": {}}
    
    
def fix_and_complete_product_name(product_name: str, inventory: list) -> str:
    """
    Fix and complete the product name based on the inventory.
    
    :param product_name: The name of the product mentioned by the user.
    :param inventory: The list of products in the inventory.
    :return: The fixed and completed product name.
    """
    items = load_all_item_names(inventory)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Completa el nombre del producto o encuentra el producto mas parecido basado en los productos disponibles en el inventario."},
                {"role": "user", "content": product_name}
            ] + [{"role": "assistant", "content": item} for item in items],
            temperature=0.7,
            max_tokens=150
        )
        completed_product_name = response.choices[0].message.content
        return completed_product_name
    except Exception as e:
        print(f"Error completando el nombre del producto: {e}")
        return product_name
    
def answer_general_consult(inventory: list, userRequest: str) -> str:
    """
    Generate a general response based on user request, but quickly lead them to see the products available in the inventory, and suggest products that match their request. 
    
    :param inventory: The list of products in the inventory.
    :return: 
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Resuelve la pregunta general del usuario de forma super rápida, pero redirige la conversación hacia los productos disponibles en el inventario y sugiere productos que coincidan con su solicitud."},
                {"role": "user", "content": userRequest}
                ],
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generando respuesta general: {e}")
        return (
            "Lo siento, hubo un error procesando tu solicitud. "
            "Aquí está lo que tenemos actualmente en stock:\n" +
            "\n".join(
                f"{producto['name']} - {producto['quantity']} en stock (${producto.get('price', 'N/A')})"
                for producto in inventory if producto["quantity"] > 0
            )
        )

def answer_suggestion_request(userRequest: str, inventory: list, entities: list) -> str:
    """
    Generate a response to a user's request for a product suggestion based on the available
    inventory and especially considering the entities extracted from the user's request.
    This version leverages an OpenAI call to find the best matching product.
    
    :param userRequest: The user's request text.
    :param inventory: The list of products in the inventory (each item is a dict with at least 'name', 'quantity').
    :param entities: The list of entities extracted from the user's request.
    :return: A product suggestion and a very brief reason (under 10 words).
    """
    try:
        # Preparamos solo los productos que tienen stock
        available_products = [prod for prod in inventory if prod["quantity"] > 0]
        if not available_products:
            return "Lo siento, no tenemos productos disponibles en este momento."
        
        # Convertimos el inventario en un string estructurado para enviarlo al prompt
        inventory_str = "\n".join(f"Producto: {p['name']}" for p in available_products)

        # Hacemos la llamada a OpenAI para que identifique el mejor match
        # Pedimos que retorne únicamente el nombre del producto con el mejor match
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente que sugiere productos basados en un inventario. "
                        "Solo responde con el nombre del producto que mejor coincida con la petición."
                    )
                },
                {
                    "role": "developer",
                    "content": (
                        "Aquí está la lista de productos disponibles (nombre):\n" + inventory_str
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Mi petición: {userRequest}\n"
                        f"Entidades relevantes: {', '.join(entities)}"
                    )
                }
            ]
        )

        # Tomamos el nombre del producto que OpenAI ha determinado como mejor match
        chosen_product_name = completion.choices[0].message.content.strip()

        # Construimos la razón (máximo 10 palabras)
        # Ajustar según lo que necesites como justificación breve
        reason = "Encaja con tu búsqueda."

        return f"{chosen_product_name}. {reason}"

    except Exception as e:
        print(f"Error generando respuesta de sugerencia: {e}")
        return (
            "Lo siento, hubo un error procesando tu solicitud. "
            "Aquí está lo que tenemos actualmente en stock:\n" +
            "\n".join(
                f"{producto['name']} - {producto['quantity']} en stock (${producto.get('price', 'N/A')})"
                for producto in inventory if producto["quantity"] > 0
            )
        )

def answer_description_request(context: str) -> str:
    """
    Basado en el contexto de la conversación, identifica el último producto mencionado por el asistente (IA)
    y devuelve su descripción. El asistente solo tiene la capacidad de mencionar productos
    que existen en el inventario actual.

    :param context: Texto que representa la conversación completa hasta este momento.
    :return: La descripción del producto mencionado o un mensaje de fallback si no se encuentra.
    """
    try:
        # 1. Instruir a la IA para que devuelva únicamente el nombre del último producto mencionado por ella misma (la IA)
        system_prompt = (
            "Eres un asistente que analiza el contexto completo de la conversación. "
            "Identifica el ÚLTIMO producto mencionado por el asistente (IA) por nombre. "
            "Devuelve ÚNICAMENTE JSON válido en el formato: {\"product_name\": \"...\"}. "
            "Si no se mencionó ningún producto, pon \"product_name\" como una cadena vacía."
        )

        # 2. Hacer la llamada a la API de OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Este es el contexto de la conversación:\n\n{context}\n\n"
                        "Por favor, extrae el último nombre de producto que el asistente mencionó."
                    )
                }
            ]
        )

        # 3. Parsear la respuesta en formato JSON para obtener el nombre del producto
        content = response.choices[0].message.content.strip()
        data = json.loads(content)
        product_name = data.get("product_name", "").strip()

        # 4. Si no hay nombre de producto, devolvemos un fallback
        if not product_name:
            return "No se encontró ningún producto mencionado recientemente por el asistente."

        # 5. Buscar el producto en el inventario
        product_description = None
        for item in inventory:
            if item["name"].lower() == product_name.lower():
                product_description = item["description"]
                break

        # 6. Retornar la descripción si la encontramos
        if product_description:
            return product_description
        else:
            return f"Lo siento, no encontré '{product_name}' en el inventario actual."

    except json.JSONDecodeError:
        return (
            "Lo siento, ocurrió un error al interpretar el nombre del producto. "
            "No tengo una descripción disponible en este momento."
        )
    except Exception as e:
        print(f"Error en 'answer_description_request': {e}")
        return "Ocurrió un error al obtener la descripción del producto."



@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Initialize conversation context and load inventory
        context = [
            {"role": "system", "content": "Eres un asistente útil que gestiona un sistema de inventario. Tu objetivo principal es ayudar a los usuarios a comprar productos que esten especificamente dentro de nuestro stock de inventario. Si un usuario pregunta sobre temas no relacionados, responde educadamente y redirige la conversación a los productos disponibles en el inventario."}
        ]
        inventory = load_inventory()

        while True:
            # Receive message from the user
            user_message = await websocket.receive_text()
            print(f"Usuario: {user_message}")

            # Extract intent and entities using OpenAI
            extracted_data = extract_intent_and_entities(user_message, context, inventory)
            intent = extracted_data.get("intent", "desconocido")
            entities = extracted_data.get("entities", {})
            
            print("-----")
            print(f"Intent: {intent}")
            print(f"Entities: {entities}")
            print("-----")

            # Add the user's message to the context
            context.append({"role": "user", "content": user_message})

            # Default value for ai_message in case no conditions are satisfied
            ai_message = "Lo siento, no entendí completamente tu solicitud. "

            # Handle inventory-related intents
            if intent == "consulta_inventario":

                categoria = entities.get("category")
                marca = entities.get("brand")
                precio_maximo = entities.get("max_price")

                if categoria:
                    # Filtrar productos por categoría
                    productos_filtrados = filter_by_category(categoria, inventory)
                    if marca:
                        # Filtrar más por marca
                        productos_filtrados = [
                            producto for producto in productos_filtrados if marca.lower() in producto["name"].lower()
                        ]
                    if precio_maximo:
                        # Filtrar más por precio
                        productos_filtrados = [
                            producto for producto in productos_filtrados if producto.get("price", float("inf")) <= precio_maximo
                        ]

                    if productos_filtrados:
                        # Formatear detalles de los productos para la respuesta
                        detalles_productos = [
                            f"{producto['name']} - {producto['quantity']} en stock (${producto.get('price', 'N/A')})"
                            for producto in productos_filtrados
                        ]
                        ai_message = (
                            f"Aquí están los {categoria}s que coinciden con tu consulta:\n" + "\n".join(detalles_productos) +
                            "\n¿Te gustaría proceder con la compra de alguno de estos?"
                        )
                    else:
                        ai_message = f"Lo siento, no tenemos {categoria}s que coincidan con tu consulta."
                else:
                    ai_message = (
                        "¿Podrías especificar qué estás buscando, como laptops o monitores? "
                        "Aquí tienes una descripción general de lo que tenemos en stock:\n" +
                        ", ".join(set(producto["category"] for producto in inventory if producto["quantity"] > 0))
                    )

            elif intent == "consulta_general":
                ai_message =  answer_general_consult(inventory, user_message)
                
            elif intent == "pedir_sugerencia":
                ai_message = answer_suggestion_request(user_message, inventory, entities)


            elif intent == "desconocido":
                # Redirigir conversaciones fuera de tema
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=context + [
                            {"role": "system", "content": "Siempre redirige la conversación hacia los productos disponibles en stock, incluso si la consulta es no relacionada."},
                            {"role": "user", "content": user_message}
                        ],
                        temperature=0.7,
                        max_tokens=150
                    )
                    ai_message = response.choices[0].message.content
                    ai_message += "\nPor cierto, si buscas algo en nuestro inventario, aquí tienes algunas opciones populares:\n" + \
                        "\n".join(
                            f"{producto['name']} - {producto['quantity']} en stock (${producto.get('price', 'N/A')})"
                            for producto in inventory[:5] if producto["quantity"] > 0
                        )
                except Exception as e:
                    print(f"Error generando respuesta de OpenAI: {e}")
                    ai_message = (
                        "Lo siento, hubo un error procesando tu solicitud. "
                        "Aquí está lo que tenemos actualmente en stock:\n" +
                        "\n".join(
                            f"{producto['name']} - {producto['quantity']} en stock (${producto.get('price', 'N/A')})"
                            for producto in inventory if producto["quantity"] > 0
                        )
                    )
            elif intent == "descripcion":
                ai_message = answer_description_request(user_message)
                        
            elif intent == "compra":
                producto = entities.get("product")
                cantidad = entities.get("quantity")
                if producto:
                    producto = fix_and_complete_product_name(producto, inventory)
                    item = find_item_by_name(producto, inventory)
                    if item:
                        if cantidad:
                            ai_message = f"¡Perfecto! Agregué {cantidad} {producto} a tu carrito de compras."
                        else:
                            ai_message = f"¡Perfecto! Agregué 1 {producto} a tu carrito de compras."
                    else:
                        ai_message = f"Lo siento, no encontré ningún producto similar a {producto} en nuestro inventario."
                else:
                    ai_message = "¿Qué producto te gustaría comprar? Por favor, proporciona el nombre del producto."
            else:
                ai_message = "Lo siento, no entendí completamente tu solicitud. ¿Podrías ser más específico o preguntar de otra manera?"
                        
            
            # Agregar la respuesta del asistente al contexto y enviarla
            context.append({"role": "assistant", "content": ai_message})
            await manager.broadcast(f"AI: {ai_message}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Cliente desconectado")