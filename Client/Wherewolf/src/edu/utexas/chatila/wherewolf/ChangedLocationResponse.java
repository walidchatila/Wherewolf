package edu.utexas.chatila.wherewolf;

public class ChangedLocationResponse extends BasicResponse {
	private int gameID;
	public ChangedLocationResponse(String status, String errorMessage, int gameID) {
		super(status, errorMessage);
		this.gameID = gameID;
	}
	
	public int getGameID(){
		return gameID;
	}
}