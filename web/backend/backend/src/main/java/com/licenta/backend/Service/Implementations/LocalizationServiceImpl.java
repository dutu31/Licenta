package com.licenta.backend.Service.Implementations;

import com.licenta.backend.Model.LocalizationRecord;
import com.licenta.backend.Repository.LocalizationRecordRepository;
import com.licenta.backend.Service.LocalizationService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class LocalizationServiceImpl implements LocalizationService {
    private final LocalizationRecordRepository localizationRecordRepository;

    @Override
    public LocalizationRecord createAndSaveRecord(String uploaderId) {
        LocalizationRecord record=LocalizationRecord.builder()
                .uploaderId(uploaderId)
                .uploadDateTime(LocalDateTime.now())
                .status("UPLOADED")
                .build();
        return localizationRecordRepository.save(record);

    }

    @Override
    public void updateStatus(Long recordId, String newStatus) {
        localizationRecordRepository.findById(recordId).ifPresent(localizationRecord -> {
            localizationRecord.setStatus(newStatus);
            localizationRecordRepository.save(localizationRecord);
        });
    }
}
