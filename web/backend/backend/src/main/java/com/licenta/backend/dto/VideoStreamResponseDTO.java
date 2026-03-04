package com.licenta.backend.dto;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class VideoStreamResponseDTO {
    private Long id;
    private String filename;
    private String filepath;
    private String uploaderId;
    private String roadSegment;
    private LocalDateTime uploadedAt;
    private Boolean isProcessed;
}
