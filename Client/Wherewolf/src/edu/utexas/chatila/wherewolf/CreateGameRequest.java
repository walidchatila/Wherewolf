package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

public class CreateGameRequest extends BasicRequest {

	  private final String gameName;
	  private final String gameDescription;
	  
	  public CreateGameRequest(String username, String password,
	          String gameName, String gameDescription) {
	      
	      super(username, password);
	      
	      this.gameName = gameName;
	      this.gameDescription = gameDescription;
	  }

	  public String getGameName() {
	      return gameName;
	  }
	  
	  public String getGameDescription() {
	      return gameDescription;
	  }


	  @Override
	  public String getURL() {
	      return "/v1/game";
	  }
	  
	  @Override
	  public RequestType getRequestType()
	  {
	      return RequestType.POST;
	  }

	  @Override
	  public List<NameValuePair> getParameters() {
	      List<NameValuePair> urlParameters = new ArrayList<NameValuePair>();
	      urlParameters.add(new BasicNameValuePair("game_name", gameName));
	      urlParameters.add(new BasicNameValuePair("description", gameDescription));
	      return urlParameters;
	  }
	  
	  /*
	  public CreateGameResponse processResponse(JSONObject jObject) throws JSONException
	  {
	      
	      JSONObject jResults = jObject.getJSONObject("results");
	      int gameID = jResults.getInt("game_id");

	      return new CreateGameResponse("success",
	              "Successfully created the game",
	              gameID);
	  }*/

	  @Override
	  public CreateGameResponse execute(WherewolfNetworking net) {
	      
	      try {
	          JSONObject jObject = net.sendRequest(this);
	          String status = jObject.getString("status");
	          
	          JSONObject jResults = jObject.getJSONObject("results");
		      int gameID = jResults.getInt("game_id");

		      
	          
	          
	          if (status.equals("success"))
	          {
	        	  return new CreateGameResponse("success",
			              "Successfully created the game",
			              gameID);
	          } else {
	              String errorMessage = jObject.getString("error");
	              return new CreateGameResponse("failure", errorMessage);
	          }
	          
	      } catch (WherewolfNetworkException ex)
	      {
	          return new CreateGameResponse("failure", "could not communicate with server.");
	      } catch (JSONException e) {
	          return new CreateGameResponse("failure", "could not parse JSON.");
	      }
	      
	  }
	  
	}