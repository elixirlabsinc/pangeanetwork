class CoOpsController < ApplicationController
  def index
    @co_ops = CoOp.all
  end
end
