package com.licenta.backend.dto;

import lombok.Data;

@Data
public class VideoMetadataRequest {   //JSON that comes from frontend
    private String filename;
    private String filepath;
    private String uploaderId;
    private String roadSegment;

}
