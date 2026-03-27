package com.licenta.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class LocalizationDTO {
    private Long id;
    private String uploaderId;
    private LocalDateTime uploadDateTime;
    private String status;
}
