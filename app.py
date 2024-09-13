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
    alignment = play_request.alignment
    if (ahead := play_request.alignment_ahead()) and not alignment:
        alignment = ahead.other()
    if not alignment:
        raise ValueError(
            "Alignment is not present and cannot be inferred from board state"
        )
    play = None
    if (state := play_request.state()) == BoardState.ONGOING:
        play = AIPlayer().get_play(board=play_request, alignment=alignment)
    return PlayResponse(status=state, play=play)
