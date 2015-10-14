package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class GetGameRequest extends BasicRequest{
	
	public GetGameRequest(String username, String password){
		super(username, password);
	}
	
	@Override
	public String getURL(){
		return "/v1/games"; 
	}
	
	@Override
	public List<NameValuePair> getParameters(){
		return null;
	}

	@Override
	public RequestType getRequestType(){
		return RequestType.GET;
	}
	
	@Override
	public GetGameResponse execute(WherewolfNetworking net){
		
		ArrayList<Games> games = new ArrayList<Games>(); 
		
		try {
			
			JSONObject jObject = net.sendRequest(this);
			
			JSONArray jArray = jObject.getJSONArray("results");
			for (int i = 0; i < jArray.length(); i++){
				try{
					JSONObject oneObject = jArray.getJSONObject(i); 
					int gameID = oneObject.getInt("game_id"); 
					String gameName = oneObject.getString("name"); 
					String gameDescription = oneObject.getString("description"); 
					
					games.add(new Games(gameID, gameName, gameDescription)); 
					
				} catch (JSONException e){
					//oops
				}
			}
		} catch (JSONException e){}
		catch (WherewolfNetworkException ex)
		{ 
			return new GetGameResponse("failure", "could not communicated with server", games);
		}
		
		return new GetGameResponse("success","got games", games);
	}
}
