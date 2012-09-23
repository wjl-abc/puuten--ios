//
//  LibViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-17.
//
//

#import <UIKit/UIKit.h>
#import "WaterFlowView.h"
#import "ImageViewCell.h"
#import "Constance.h"

@interface LibViewController : UIViewController<WaterFlowViewDelegate, WaterFlowViewDataSource>
{
    NSMutableArray *arrayData;
    NSMutableArray *array4wb;
    NSMutableDictionary *dicData;
    NSMutableDictionary *dic4wb;
    WaterFlowView  *waterFlow;
    int selected_cell;
    int selected_order;
}
@property (assign, nonatomic) NSString *categ;
- (void)dataSourceDidLoad;
- (void)dataSourceDidError;

@end
