from brownie import network, Lottery, accounts, config, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link
from web3 import Web3
import pytest

def test_get_entrance_fee():
    # account = accounts[0]
    # lottery = Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"],{"from":account})
    # assert lottery.getEntranceFee() > Web3.toWei(0.018, "ether")
    # assert lottery.getEntranceFee() < Web3.toWei(0.019, "ether")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    expected_entrance_fee = Web3.toWei(0.025,"ether")
    entrance_fee = lottery.getEntranceFee()
    # print(entrance_fee)
    # Assert
    assert expected_entrance_fee == entrance_fee

def test_cant_enter_unless_started():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
    # with pytest.raises(AttributeError):
        lottery.enter({"from":account, "value": lottery.getEntranceFee()+10000000000})
    #     lottery.enter({"from":account, "value": lottery.getEntranceFee()+10000000000})


def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    # Act
    lottery.enter({"from":account, "value":lottery.getEntranceFee()+10000000000})
    # Assert
    assert lottery.players(0) == account

def test_can_end_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value":lottery.getEntranceFee()})
    fund_with_link(lottery)
    print(f"endlottery: {lottery.endLottery}")
    transaction = lottery.endLottery({"from": account})
    # Assert
    assert lottery.lottery_state() == 2
