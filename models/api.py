from models import Board, Alignment, Play, BaseModel, BoardState, model_validator


class PlayRequest(BaseModel):
    board: Board
    alignment: Alignment | None = None

    def validate_next_play_is_valid(self) -> None:
        ahead = self.board.alignment_ahead()
        if not ahead:
            return
        if ahead == self.alignment:
            raise ValueError(
                f"{ahead} can't make a move since it's {ahead.other()}'s turn"
            )

    @model_validator(mode="after")
    def validate_play_request(self) -> "PlayRequest":
        self.validate_next_play_is_valid()
        return self


class PlayResponse(BaseModel):
    status: BoardState
    play: Play | None
