from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import BoardState
from models.api import PlayRequest, PlayResponse
from player.ai import AIPlayer


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get-play")
def get_playlist_data_endpoint(play_request: PlayRequest) -> PlayResponse:
    board = play_request.board
    alignment = play_request.alignment
    if (ahead := board.alignment_ahead()) and not alignment:
        alignment = ahead.other()
    if (state := board.state()) == BoardState.ONGOING:
        play = AIPlayer().get_play(board=board, alignment=alignment)
    return PlayResponse(status=state, play=play)
