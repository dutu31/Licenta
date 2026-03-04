package com.licenta.backend.Converter;

import com.licenta.backend.Model.VideoStream;
import com.licenta.backend.dto.VideoStreamResponseDTO;
import org.springframework.stereotype.Component;

@Component
public class VideoStreamConverter {
    public VideoStreamResponseDTO toDTO(VideoStream videoStream) {
        VideoStreamResponseDTO dto = new VideoStreamResponseDTO();
        dto.setId(videoStream.getId());
        dto.setFilename(videoStream.getFilename());
        dto.setFilepath(videoStream.getFilepath());
        dto.setUploaderId(videoStream.getUploaderId());
        dto.setUploadedAt(videoStream.getUploadedAt());
        dto.setRoadSegment(videoStream.getRoadSegment());
        dto.setIsProcessed(videoStream.getIsProcessed());
        return dto;
    }
}
