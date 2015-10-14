package edu.utexas.chatila.wherewolf;


public class Games {
	
	private int game_id;
	private String name;
	private String description;
	
	public Games(int game_id, String name, String description){
		this.game_id = game_id;
		this.name = name;
		this.description = description;
	}
	
	public int getGameId(){
		return game_id;
	}

	public void setGameId(){
		this.game_id = game_id;
	}
	public String getName() {
		return name;
	}
	
	@Override
	public String toString(){
		return name; 
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}
	
	
}
