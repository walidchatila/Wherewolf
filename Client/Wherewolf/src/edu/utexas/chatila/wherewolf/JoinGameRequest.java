package edu.utexas.chatila.wherewolf;

import java.util.List;

import org.apache.http.NameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

public class JoinGameRequest extends BasicRequest{

	protected final int gameID;
	
	public JoinGameRequest(String username, String password, int gameID){
		super(username, password);
		this.gameID = gameID;
	}
	
	public int getGameID() { 
		return gameID;
	}
	
	@Override
	public String getURL()
	{
		return "/v1/game/" + Integer.toString(gameID) + "/lobby"; 
	}
	
	@Override
	public List<NameValuePair> getParameters(){
		return null;
	}
	
	@Override
	public RequestType getRequestType(){
		return RequestType.POST;
	}
	
	
	@Override
	public JoinGameResponse execute(WherewolfNetworking net){
		
		
		      
		      try { 
		    	  
		    	  JSONObject response = net.sendRequest(this);
		          
			          
		          if (response.getString("status").equals("success"))
		          {
		        	  return new JoinGameResponse("success",
				              "Successfully created the game"
				              );
		          } else {
		              String errorMessage = response.getString("error");
		              return new JoinGameResponse("failure", errorMessage);
		          }
		          
		      } catch (WherewolfNetworkException ex)
		      {
		          return new JoinGameResponse("failure", "could not communicate with server.");
		      } catch (JSONException e) {
		          return new JoinGameResponse("failure", "could not parse JSON.");
		      }
		      
		  }
}
