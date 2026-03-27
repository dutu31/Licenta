package com.licenta.backend.Converter;

import com.licenta.backend.Model.LocalizationRecord;
import com.licenta.backend.dto.LocalizationDTO;
import org.springframework.stereotype.Component;

@Component
public class LocalizationConverter {
    public LocalizationDTO entityToDTO(LocalizationRecord entity) {
        if(entity==null){
            return null;
        }
        return LocalizationDTO.builder()
                .id(entity.getId())
                .uploaderId(entity.getUploaderId())
                .uploadDateTime(entity.getUploadDateTime())
                .status(entity.getStatus())
                .build();
    }

    public LocalizationRecord dtoToEntity(LocalizationDTO dto) {
        if(dto==null){
            return null;
        }
        return LocalizationRecord.builder()
                .id(dto.getId())
                .uploaderId(dto.getUploaderId())
                .uploadDateTime(dto.getUploadDateTime())
                .status(dto.getStatus())
                .build();
    }
}
