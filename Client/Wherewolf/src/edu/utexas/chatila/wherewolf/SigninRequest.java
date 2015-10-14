package edu.utexas.chatila.wherewolf;

import java.util.List;

import org.apache.http.NameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

public class SigninRequest extends BasicRequest {

	  public SigninRequest (String username, String password)
	  {
	      super(username, password);
	  }
	  
	 
	  @Override
	  public String getURL() {
	      return "/v1/checkpassword";
	  }

	  @Override
	  public List<NameValuePair> getParameters() {
	      return null;
	  }

	  @Override
	  public RequestType getRequestType() {
	      return RequestType.GET;
	  }

	  @Override
	  public SigninResponse execute(WherewolfNetworking net) {
	  
	      try {
	          JSONObject response = net.sendRequest(this);
	          
	          if (response.getString("status").equals("success"))
	          {
	              // int playerID = response.getInt("playerid");
	              return new SigninResponse("success", "signed in successfully");
	          } else {
	              
	              String errorMessage = response.getString("error");
	              return new SigninResponse("failure", errorMessage);
	          }
	      } catch (JSONException e) {
	          return new SigninResponse("failure", "Incorrect username and or password.");
	      } catch (WherewolfNetworkException ex)
	      {
	          return new SigninResponse("failure", "Incorrect username and or password.");
	      }
	      
	      
	      
	  }

	}