require 'test_helper'

class CoOpControllerTest < ActionDispatch::IntegrationTest
  context 'index' do
    should 'get index' do
      get co_ops_path

      assert_response :success
    end
  end

  context 'show' do
    should 'get show' do
      co_op = create(:co_op)

      get co_op_path(co_op.id)

      assert_response :success
    end
  end

  context 'create' do
    should 'be able to create' do
      phase = create(:phase)
      params = { co_op: {
        name: 'co-op 1',
        phase_id: phase.id,
        is_active: true,
        start_date: 1.year.ago,
        end_date: 3.years.from_now,
        location: 'place',
        interest: 5,
        initial_balance: 5000,
        expected_repayment: 5250,
        current_balance: 3000
      } }

      assert_difference 'CoOp.count' do
        post co_ops_path(params)
      end

      assert_redirected_to co_ops_path
    end

    should 'flash error' do
      params = { co_op: {
        name: 'co-op 1',
        phase_id: create(:phase).id,
        is_active: true,
        start_date: 1.year.ago,
        end_date: 3.years.from_now,
        location: '',
        interest: 5,
        initial_balance: 5000,
        expected_repayment: 5250,
        current_balance: 3000
      } }

      assert_no_difference 'CoOp.count' do
        post co_ops_path(params)
      end

      assert_includes flash[:error], 'Location can\'t be blank'
    end
  end
end
