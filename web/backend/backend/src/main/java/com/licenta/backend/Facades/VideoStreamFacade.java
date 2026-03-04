package com.licenta.backend.Facades;

import com.licenta.backend.dto.VideoMetadataRequest;
import com.licenta.backend.dto.VideoStreamResponseDTO;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

public interface VideoStreamFacade {
    VideoStreamResponseDTO processAndSaveVideo(MultipartFile file, String uploaderId, String roadSegment) throws IOException;
    List<VideoStreamResponseDTO> getAllVideos();

}
