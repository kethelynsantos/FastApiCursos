from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi import Response
from models import Curso

app = FastAPI()  # instancia de um objeto


@app.get('/')  # agora a instancia se torna um decorador! todos os verbos http que temos! qual p método
# get que sera executado e qual sera a função que vai responder o metodo get naquele endpoint
async def raiz():
    return {"msg": "Aprendizes de DS"}


cursos = {
    1: {
        "nome": "Python",
        "aulas": 20,
        "horas": 80,
        "instrutor": "Cleber",
    },
    2: {
        "nome": "Java",
        "aulas": 15,
        "horas": 60,
        "instrutor": "Leonardo",
    }
}


@app.get('/cursos')
async def get_cursos():
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int):
    try:
        curso = cursos[curso_id]
        curso.update({"id": curso_id})
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso Não Encontrado.')


@app.post('/cursos')
async def post_curso(curso: Curso):
    curso.id = sorted(cursos.keys())[-1] + 1  # trazendo o ultumo item da lista
    cursos[curso.id] = curso
    return curso
    # else:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Já existe um curso com o ID {curso.id}")


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso):
    if curso_id in cursos:
        curso_id = curso_id
        cursos[curso_id] = curso
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Esse Curso Não Existe.')


@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Esse Curso Não Existe.')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
