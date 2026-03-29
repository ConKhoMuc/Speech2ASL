package vn.iotstar.appspeech2asl;


import okhttp3.MultipartBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;
import retrofit2.http.Path;


public interface ApiService {

    @Multipart
    @POST("/upload_audio")
    Call<VideoResponse> uploadAudio(
            @Part MultipartBody.Part audio
    );

}