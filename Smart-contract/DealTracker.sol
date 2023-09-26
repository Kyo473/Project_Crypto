// Импорт необходимых библиотек
pragma solidity ^0.8.0;

// Объявление контракта
contract DealTracker {

    // Структура для представления сделки
    struct Deal {
        address sender;    // Адрес отправителя
        address receiver;  // Адрес получателя
        uint256 amount;    // Сумма сделки
        bytes32 dealID;    // Идентификатор сделки
    }

    // Маппинг для хранения информации о сделках по их идентификатору
    mapping(bytes32 => Deal) public deals;

    // Функция для добавления новой сделки
    function addDeal(address _sender, address _receiver, uint256 _amount, bytes32 _dealID) public {
        Deal memory newDeal = Deal(_sender, _receiver, _amount, _dealID);
        deals[_dealID] = newDeal;
    }
}
